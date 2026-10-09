import copy
import base64
import importlib.util
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('refresh', Path(__file__).parents[1] / 'scripts' / 'refresh_hf_downloads.py')
refresh = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(refresh)


class DownloadTotalsTest(unittest.TestCase):
    def setUp(self):
        self.config = {'projects': {
            'first': [{'type': 'model', 'id': 'team/model'}, {'type': 'dataset', 'id': 'team/data'}],
            'second': [{'type': 'dataset', 'id': 'team/benchmark'}],
        }, 'groups': {'series': ['first', 'second']}}

    def test_totals_groups_and_zero(self):
        values = {'team/model': 11, 'team/data': 0, 'team/benchmark': 7}
        result = refresh.aggregate(self.config, lambda r: values[r['id']])
        self.assertEqual(result['team'], {'models': 11, 'datasets': 7, 'total': 18})
        self.assertEqual(result['groups']['series'], result['team'])
        self.assertEqual(result['projects']['first']['datasets'], 0)

    def test_duplicate_repository_rejected(self):
        self.config['projects']['second'].append(self.config['projects']['first'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            refresh.aggregate(self.config, lambda _: 1)

    def test_duplicate_group_member_rejected(self):
        self.config['groups']['series'].append('first')
        with self.assertRaisesRegex(ValueError, 'Invalid group'):
            refresh.aggregate(self.config, lambda _: 1)

    def test_failed_fetch_aborts_entire_snapshot(self):
        def fetch(resource):
            if resource['id'] == 'team/data':
                raise OSError('Upstream unavailable')
            return 11
        with self.assertRaises(OSError):
            refresh.aggregate(self.config, fetch)

    def test_no_fallback_to_monthly_downloads(self):
        with patch.object(refresh, 'request_json', return_value={'id': 'team/model', 'downloads': 999}):
            with self.assertRaisesRegex(ValueError, 'downloadsAllTime'):
                refresh.fetch_count({'type': 'model', 'id': 'team/model'})

    def test_invalid_counts_rejected(self):
        for value in [None, -1, True, '42', 2.5]:
            with self.subTest(value=value), patch.object(refresh, 'request_json', return_value={'id': 'team/model', 'downloadsAllTime': value}):
                with self.assertRaises(ValueError):
                    refresh.fetch_count({'type': 'model', 'id': 'team/model'})

    def test_renamed_repository_requires_registry_update(self):
        with patch.object(refresh, 'request_json', return_value={'id': 'new/model', 'downloadsAllTime': 42}):
            with self.assertRaisesRegex(ValueError, 'renamed'):
                refresh.fetch_count({'type': 'model', 'id': 'team/model'})

    def test_unchanged_values_ignore_timestamp(self):
        old = refresh.aggregate(self.config, lambda _: 1)
        new = copy.deepcopy(old)
        old['updatedAt'], new['updatedAt'] = 'earlier', 'later'
        self.assertTrue(refresh.equivalent(old, new))
        new['team']['total'] += 1
        self.assertFalse(refresh.equivalent(old, new))

    def test_publish_uses_current_sha_and_stats_branch(self):
        old = refresh.aggregate(self.config, lambda _: 1)
        new = refresh.aggregate(self.config, lambda _: 2)
        current = {'sha': 'current-blob-sha', 'content': base64.b64encode(json.dumps(old).encode()).decode()}
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'ZJU-OmniAI/.github', 'GH_TOKEN': 'test-token'}), patch.object(refresh, 'request_json', side_effect=[current, {}]) as request:
            refresh.publish(new)
        self.assertEqual(request.call_count, 2)
        body = request.call_args.kwargs['body']
        self.assertEqual(body['sha'], 'current-blob-sha')
        self.assertEqual(body['branch'], 'hf-download-stats')
        self.assertEqual(json.loads(base64.b64decode(body['content']))['team']['total'], 6)

    def test_unchanged_snapshot_does_not_write(self):
        old = refresh.aggregate(self.config, lambda _: 1)
        current = {'sha': 'current-blob-sha', 'content': base64.b64encode(json.dumps(old).encode()).decode()}
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'ZJU-OmniAI/.github', 'GH_TOKEN': 'test-token'}), patch.object(refresh, 'request_json', return_value=current) as request:
            refresh.publish(copy.deepcopy(old))
        self.assertEqual(request.call_count, 1)


if __name__ == '__main__':
    unittest.main()
