#!/usr/bin/env python3
"""Fetch all-time Hugging Face counts and atomically publish complete totals."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

STATS_BRANCH = 'hf-download-stats'
STATS_PATH = 'downloads.json'


def request_json(url, *, method='GET', body=None, token=None):
    headers = {'Accept': 'application/json', 'User-Agent': 'ZJU-OmniAI-HF-downloads/1.0'}
    if token:
        if not url.startswith('https://api.github.com/'):
            raise ValueError('GitHub credentials may only be sent to the GitHub API')
        headers['Authorization'] = f'Bearer {token}'
        headers['X-GitHub-Api-Version'] = '2022-11-28'
    data = None if body is None else json.dumps(body).encode()
    if data is not None:
        headers['Content-Type'] = 'application/json'
    for attempt in range(3):
        try:
            with urlopen(Request(url, data=data, headers=headers, method=method), timeout=20) as response:
                return json.load(response)
        except HTTPError as error:
            # Never blindly retry writes; a timeout can occur after a successful update.
            if method != 'GET' or error.code not in (408, 429, 500, 502, 503, 504) or attempt == 2:
                raise
            time.sleep(min(10, 2 ** attempt))
        except (URLError, TimeoutError):
            if method != 'GET' or attempt == 2:
                raise
            time.sleep(2 ** attempt)


def validate_config(config):
    if not isinstance(config.get('projects'), dict) or not config['projects']:
        raise ValueError('At least one project is required')
    seen = set()
    for project, resources in config['projects'].items():
        if not re.fullmatch(r'[a-z0-9-]+', project) or not resources:
            raise ValueError(f'Invalid project: {project}')
        for resource in resources:
            kind, repo_id = resource['type'], resource['id']
            if kind not in ('model', 'dataset') or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo_id):
                raise ValueError(f'Invalid resource: {resource}')
            key = kind + ':' + repo_id
            if key in seen:
                raise ValueError(f'Duplicate resource would inflate totals: {key}')
            seen.add(key)
    for name, members in config.get('groups', {}).items():
        if not members or len(members) != len(set(members)) or any(x not in config['projects'] for x in members):
            raise ValueError(f'Invalid group: {name}')


def fetch_count(resource):
    query = urlencode({'expand[]': 'downloadsAllTime'})
    url = f'https://huggingface.co/api/{resource["type"]}s/{quote(resource["id"], safe="/")}?{query}'
    data = request_json(url)
    count = data.get('downloadsAllTime')
    if type(count) is not int or count < 0:
        raise ValueError(f'Missing or invalid downloadsAllTime for {resource["id"]}')
    if data.get('id') != resource['id']:
        raise ValueError(f'Repository was renamed; update the registry before publishing: {resource["id"]}')
    return count


def aggregate(config, fetch=fetch_count):
    validate_config(config)
    resources = [r for rows in config['projects'].values() for r in rows]
    # A missing/failed repository aborts the entire refresh, preserving the last complete snapshot.
    with ThreadPoolExecutor(max_workers=4) as pool:
        values = list(pool.map(fetch, resources))
    for count in values:
        if type(count) is not int or count < 0:
            raise ValueError('Download counts must be non-negative integers')
    counts = {r['type'] + ':' + r['id']: count for r, count in zip(resources, values)}

    def summarize(rows):
        models = sum(counts['model:' + r['id']] for r in rows if r['type'] == 'model')
        datasets = sum(counts['dataset:' + r['id']] for r in rows if r['type'] == 'dataset')
        return {'models': models, 'datasets': datasets, 'total': models + datasets}

    projects = {name: summarize(rows) for name, rows in config['projects'].items()}
    groups = {name: summarize([r for member in members for r in config['projects'][member]]) for name, members in config.get('groups', {}).items()}
    return {'schemaVersion': 1, 'metric': 'downloadsAllTime', 'resources': counts, 'projects': projects, 'groups': groups, 'team': summarize(resources)}


def equivalent(old, new):
    return {k: v for k, v in old.items() if k != 'updatedAt'} == {k: v for k, v in new.items() if k != 'updatedAt'}


def publish(snapshot):
    repo = os.environ['GITHUB_REPOSITORY']
    if repo != 'ZJU-OmniAI/.github':
        raise ValueError('Publishing is restricted to ZJU-OmniAI/.github')
    token = os.environ['GH_TOKEN']
    endpoint = f'https://api.github.com/repos/{repo}/contents/{STATS_PATH}'
    current = request_json(endpoint + '?' + urlencode({'ref': STATS_BRANCH}), token=token)
    previous = json.loads(base64.b64decode(current['content']))
    if equivalent(previous, snapshot):
        print('Counts unchanged; keeping the existing snapshot without a new commit.')
        return
    snapshot['updatedAt'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    content = json.dumps(snapshot, indent=2, sort_keys=True) + '\n'
    request_json(endpoint, method='PUT', token=token, body={
        'message': 'chore: refresh all-time Hugging Face download totals',
        'branch': STATS_BRANCH,
        'sha': current['sha'],
        'content': base64.b64encode(content.encode()).decode(),
    })
    print('Published complete download totals to the generated stats branch.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='metrics/huggingface-repositories.json')
    parser.add_argument('--output')
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    snapshot = aggregate(json.loads(Path(args.config).read_text()))
    snapshot['updatedAt'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    if args.output:
        Path(args.output).write_text(json.dumps(snapshot, indent=2, sort_keys=True) + '\n')
    if args.publish:
        publish(snapshot)
    print(json.dumps(snapshot['team'], sort_keys=True))


if __name__ == '__main__':
    main()
