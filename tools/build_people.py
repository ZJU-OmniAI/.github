#!/usr/bin/env python3
"""Build people/README.md and round avatars from people/people.json.

    python3 tools/build_people.py

Each person may have: name, name_zh, title, role, year, works (list), photo
(a file in people/photos/), homepage, scholar, github, x, email.
Without `photo` the card shows the shared placeholder avatar; set
"github_avatar": true to use the GitHub picture instead.
Edit people.json and rerun; never hand-edit people/README.md or people/avatars/.
"""
from __future__ import annotations

import html
import io
import json
import re
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = ROOT / 'people'
AVATARS = PEOPLE / 'avatars'
ICONS = ROOT / 'profile' / 'assets' / 'icons'
ORG = 'https://github.com/ZJU-OmniAI'
SIZE = 320
RING = ((5, 73, 160), (92, 192, 250))  # OmniAI ring gradient, matches the banner

ICON_PATHS: dict[str, str] = {
    'homepage': '<path d="M3 11 12 4l9 7M5 10v10h5v-6h4v6h5V10"/>',
    'scholar': '<path d="M12 4 2 9.5 12 15l10-5.5L12 4Z"/><path d="M6 12v4.5c0 1.6 2.7 3 6 3s6-1.4 6-3V12"/>',
    'github': '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    'x': '<path d="M4 4l16 16M20 4 4 20"/>',
    'email': '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
}
ICON_TITLES = {'homepage': 'Homepage', 'scholar': 'Google Scholar', 'github': 'GitHub', 'x': 'X', 'email': 'Email'}


def write_icons() -> None:
    """Mid-tone icons that read on both GitHub's light and dark backgrounds."""
    ICONS.mkdir(parents=True, exist_ok=True)
    for name, d in ICON_PATHS.items():
        (ICONS / f'{name}.svg').write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" '
            f'stroke="#5B8DEF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</svg>\n')


def slug(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def _gradient(size: int, c0: tuple[int, int, int], c1: tuple[int, int, int]) -> Image.Image:
    im = Image.new('RGB', (size, size))
    px = im.load()
    for y in range(size):
        for x in range(size):
            t = (x + (size - y)) / (2 * size)
            px[x, y] = tuple(int(c0[c] + (c1[c] - c0[c]) * t) for c in range(3))  # type: ignore[index]
    return im


def _placeholder(big: int) -> Image.Image:
    """Soft blue disc with a person silhouette: reads as 'photo to come' on light and dark pages."""
    im = _gradient(big, (226, 236, 250), (205, 224, 248))
    d = ImageDraw.Draw(im)
    c = big / 2
    col = (150, 178, 218)
    r = big * 0.17
    d.ellipse((c - r, big * 0.24, c + r, big * 0.24 + 2 * r), fill=col)
    d.ellipse((c - big * 0.32, big * 0.62, c + big * 0.32, big * 1.18), fill=col)
    return im


def _square(im: Image.Image) -> Image.Image:
    w, h = im.size
    side = min(w, h)
    top = 0 if h > w else (h - side) // 2  # portraits: keep the face near the top
    return im.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side))


def _face(person: dict[str, object], big: int) -> tuple[Image.Image, str]:
    photo = person.get('photo')
    if photo:
        return _square(Image.open(PEOPLE / 'photos' / str(photo)).convert('RGB')).resize((big, big), Image.LANCZOS), slug(str(person['name']))
    login = person.get('github')
    if login and person.get('github_avatar'):
        req = urllib.request.Request(f'https://github.com/{login}.png?size={SIZE}', headers={'User-Agent': 'ZJU-OmniAI-people/1.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            img = Image.open(io.BytesIO(r.read())).convert('RGB')
        return _square(img).resize((big, big), Image.LANCZOS), slug(str(person['name']))
    return _placeholder(big), '_placeholder'


def avatar(person: dict[str, object]) -> str:
    """Round avatar with a thin OmniAI-gradient ring, transparent outside."""
    AVATARS.mkdir(parents=True, exist_ok=True)
    scale = 3  # draw large, then downsample for smooth edges
    big = SIZE * scale
    face, name = _face(person, big)
    path = AVATARS / f'{name}.png'
    if name == '_placeholder' and path.exists():
        return f'avatars/{path.name}'
    out = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    outer = Image.new('L', (big, big), 0)
    ImageDraw.Draw(outer).ellipse((0, 0, big - 1, big - 1), fill=255)
    out.paste(_gradient(big, RING[0], RING[1]), (0, 0), outer)
    pad = 7 * scale
    inner = Image.new('L', (big, big), 0)
    ImageDraw.Draw(inner).ellipse((pad, pad, big - 1 - pad, big - 1 - pad), fill=255)
    out.paste(face, (0, 0), inner)
    out.resize((SIZE, SIZE), Image.LANCZOS).save(path, optimize=True)
    return f'avatars/{path.name}'


def links(person: dict[str, object], size: int = 18) -> str:
    out = []
    for key in ('homepage', 'scholar', 'github', 'x', 'email'):
        val = person.get(key)
        if not val:
            continue
        url = {'github': f'https://github.com/{val}', 'x': f'https://x.com/{val}', 'email': f'mailto:{val}'}.get(key, str(val))
        out.append(f'<a href="{html.escape(url)}" title="{ICON_TITLES[key]}"><img src="../profile/assets/icons/{key}.svg" '
                   f'alt="{ICON_TITLES[key]}" width="{size}" height="{size}"></a>')
    return '&nbsp;&nbsp;'.join(out)


def _name(p: dict[str, object]) -> str:
    name = html.escape(str(p['name']))
    if p.get('homepage'):
        name = f'<a href="{html.escape(str(p["homepage"]))}">{name}</a>'
    return name


def card(p: dict[str, object], group_role: str, width: int, avatar_w: int, big: bool = False) -> str:
    parts = [f'<img src="{avatar(p)}" alt="{html.escape(str(p["name"]))}" width="{avatar_w}"><br>']
    zh = f' · {html.escape(str(p["name_zh"]))}' if p.get('name_zh') else ''
    parts.append(f'<h3>{_name(p)}{zh}</h3>' if big else f'<b>{_name(p)}</b>{zh}<br>')
    role = str(p.get('title') or p.get('role') or group_role)
    detail = ' · '.join(x for x in (role, str(p.get('year') or '')) if x)
    if detail:
        parts.append(f'<sub>{html.escape(detail)}</sub><br>')
    if p.get('works'):
        parts.append(f'<sub>{" · ".join(html.escape(str(w)) for w in p["works"])}</sub><br>')  # type: ignore[union-attr]
    icons = links(p, 20 if big else 18)
    if icons:
        parts.append(icons)
    return f'<td align="center" valign="top" width="{width}%">{"".join(parts)}</td>'


def grid(members: list[dict[str, object]], role: str, cols: int, avatar_w: int, big: bool = False) -> str:
    rows = []
    w = 100 // cols
    for i in range(0, len(members), cols):
        cells = [card(m, role, w, avatar_w, big) for m in members[i:i + cols]]
        cells += [f'<td width="{w}%"></td>'] * (cols - len(cells))
        rows.append('<tr>' + ''.join(cells) + '</tr>')
    return '<table>\n' + '\n'.join(rows) + '\n</table>'


def picture(name: str, alt: str, height: str = '') -> str:
    h = f' height="{height}"' if height else ' width="100%"'
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="../profile/assets/{name}-dark.svg">'
            f'<img alt="{alt}" src="../profile/assets/{name}-light.svg"{h}></picture>')


def build() -> str:
    data = json.loads((PEOPLE / 'people.json').read_text())
    out: list[str] = ['<!-- Generated by tools/build_people.py from people/people.json. Do not edit by hand. -->', '<div align="center">', '',
                      f'<p>{picture("people-banner", "ZJU-OmniAI people")}</p>', '',
                      f'<a href="{ORG}">{picture("links/home", "Back to homepage", "28")}</a>', '', '</div>', '']
    for key in ('intro', 'intro_zh'):
        if data.get(key):
            out += [str(data[key]), '']
    if data.get('note'):
        out += [f'<sub>{data["note"]}</sub>', '']
    for group in data.get('groups', []):
        members = group.get('members') or []
        if not members:
            continue
        big = bool(group.get('featured'))
        out += [f'### {group["title"]}', '',
                grid(members, str(group.get('role', '')), int(group.get('columns', 2 if big else 4)), 150 if big else 104, big), '']
    alumni = data.get('alumni') or []
    if alumni:
        rows = ''.join(
            f'<tr><td>{html.escape(a["name"])}{" · " + html.escape(a["name_zh"]) if a.get("name_zh") else ""}</td>'
            f'<td>{html.escape(a.get("degree", ""))}</td><td>{html.escape(a.get("now", ""))}</td></tr>' for a in alumni)
        out += ['### Alumni · 毕业生', '', f'<table><tr><th align="left">Name</th><th align="left">Degree</th><th align="left">Now</th></tr>{rows}</table>', '']
    out += [picture('divider', ''), '', '<div align="center">', '<br>']
    if data.get('join'):
        out += [str(data['join']), '<br><br>']
    out += [f'<a href="{ORG}">{picture("links/home", "Homepage", "28")}</a>&nbsp;',
            f'<a href="https://github.com/orgs/ZJU-OmniAI/repositories">{picture("links/repos", "All Repositories", "28")}</a>&nbsp;',
            f'<a href="https://huggingface.co/OmniAI-ZJU">{picture("links/huggingface", "Hugging Face", "28")}</a>&nbsp;',
            f'<a href="mailto:{data.get("contact", "")}">{picture("links/contact", "Contact", "28")}</a>', '</div>', '']
    return '\n'.join(out)


def main() -> None:
    write_icons()
    (PEOPLE / 'README.md').write_text(build())
    print('wrote', (PEOPLE / 'README.md').relative_to(ROOT), 'and', len(list(AVATARS.glob('*.png'))), 'avatar files')


if __name__ == '__main__':
    main()
