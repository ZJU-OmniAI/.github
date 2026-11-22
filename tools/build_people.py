#!/usr/bin/env python3
"""Build the People page (people/README.md) and its graphics from people/people.json.

    INTER_DIR=... NOTO_SC_DIR=... python3 tools/build_people.py

The layout follows zjureal.com/people.html: a hero with the group photo, faculty
cards with the portrait beside the details, then a borderless grid of member
cards under small section labels.

people.json:
  hero_en, hero_zh   text in the hero
  note               small line under the hero
  group_photos       files in people/photos/ that rotate in the hero (placeholder if empty)
  groups             [{title: "PhD Students · 博士生", featured?: true, members: [...]}]
  alumni             [{name, name_zh, degree, now}]
Each person may have: name, name_zh, title, role, year, works (list), photo
(a file in people/photos/), homepage, scholar (full URL), github, x, email.
Without `photo` the portrait shows the person's initials, as zjureal.com does.
Edit people.json and rerun; never hand-edit people/README.md or people/assets/.
"""
from __future__ import annotations

import base64
import html
import io
import json
import re
import shutil
from pathlib import Path

from PIL import Image, ImageOps

from build_profile_assets import DARK, LIGHT, PILLARS, Theme, loop, ring_gradient, svg_doc
from svgtext import GlyphDefs, measure, text, text_baked

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = ROOT / 'people'
PHOTOS = PEOPLE / 'photos'
ASSETS = PEOPLE / 'assets'
ICONS = ROOT / 'profile' / 'assets' / 'icons'
ORG = 'https://github.com/ZJU-OmniAI'
THEMES = (LIGHT, DARK)
PILL, FULL = 'height="28"', 'width="100%"'

ICON_PATHS: dict[str, str] = {
    'homepage': '<path d="M3 11 12 4l9 7M5 10v10h5v-6h4v6h5V10"/>',
    'scholar': '<path d="M12 4 2 9.5 12 15l10-5.5L12 4Z"/><path d="M6 12v4.5c0 1.6 2.7 3 6 3s6-1.4 6-3V12"/>',
    'github': '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    'x': '<path d="M4 4l16 16M20 4 4 20"/>',
    'email': '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
}
ICON_TITLES = {'homepage': 'Homepage', 'scholar': 'Google Scholar', 'github': 'GitHub', 'x': 'X', 'email': 'Email'}
# Portrait placeholder tiles: (top-left, bottom-right, edge)
TILE = {'light': ('#EEF4FD', '#D9E6F8', '#D3E1F4'), 'dark': ('#14233B', '#1B3254', '#27406A')}
SHADOW = {'light': ('#0B2447', '.14'), 'dark': ('#000000', '.5')}
CJK = r'⺀-鿿　-〿＀-￯'
NO_BREAK_BEFORE = set('，。、；：！？）》」』')

Person = dict[str, object]


# ---------------------------------------------------------------- helpers

def write_icons() -> None:
    """Mid-tone link icons that read on both GitHub's light and dark backgrounds."""
    ICONS.mkdir(parents=True, exist_ok=True)
    for name, d in ICON_PATHS.items():
        (ICONS / f'{name}.svg').write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" '
            f'stroke="#5B8DEF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</svg>\n')


def slug(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def section_slug(title: str) -> str:
    return slug(title.partition(' · ')[0])


def initials(name: str) -> str:
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def wrap(s: str, size: float, weight: int, max_w: float) -> list[str]:
    """Greedy line breaking: Latin breaks at spaces, CJK between characters."""
    tokens = re.findall(rf'[{CJK}]|[^\s{CJK}]+|\s+', s)
    lines: list[str] = []
    cur = ''
    for tok in tokens:
        trial = cur + tok
        if cur.strip() and not tok.isspace() and tok not in NO_BREAK_BEFORE and measure(trial.rstrip(), size, weight) > max_w:
            lines.append(cur.rstrip())
            cur = tok
        else:
            cur = trial
    if cur.strip():
        lines.append(cur.strip())
    return lines


def fit(s: str, size: float, weight: int, max_w: float, min_size: float) -> float:
    while size > min_size and measure(s, size, weight) > max_w:
        size -= 0.5
    return size


def jpeg_uri(path: Path, w: int, h: int) -> str:
    """Crop to w:h (portraits keep the face near the top), resize, and inline as base64 JPEG."""
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    iw, ih = im.size
    if iw / ih > w / h:
        nw = round(ih * w / h)
        box = ((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih)
    else:
        nh = round(iw * h / w)
        top = round((ih - nh) * (0.2 if w == h else 0.5))
        box = (0, top, iw, top + nh)
    buf = io.BytesIO()
    im.crop(box).resize((w, h), Image.LANCZOS).save(buf, 'JPEG', quality=84, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def accent(t: Theme) -> str:
    return t.brand[0] if t.name == 'light' else t.brand[1]


# ---------------------------------------------------------------- graphics

def portrait(t: Theme, p: Person, x: float, y: float, s: float, uid: str, defs: GlyphDefs, delay: float) -> tuple[str, str]:
    """Rounded-square portrait; initials on a soft tile with a passing sheen until a photo arrives.

    Returns (defs markup, body markup).
    """
    r = s * 0.06
    c0, c1, edge = TILE[t.name]
    d = [f'<clipPath id="f{uid}"><rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r:.1f}"/></clipPath>']
    if p.get('photo'):
        px = round(s * 1.0)
        body = (f'<image href="{jpeg_uri(PHOTOS / str(p["photo"]), px, px)}" x="{x}" y="{y}" width="{s}" height="{s}" '
                f'preserveAspectRatio="xMidYMid slice" clip-path="url(#f{uid})"/>')
    else:
        d.append(f'<linearGradient id="t{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c0}"/>'
                 f'<stop offset="1" stop-color="{c1}"/></linearGradient>'
                 f'<linearGradient id="s{uid}" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
                 f'<stop offset=".5" stop-color="#FFFFFF" stop-opacity="{".6" if t.name == "light" else ".07"}"/>'
                 f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
        letters, _ = text(defs, initials(str(p['name'])), x + s / 2, y + s / 2 + s * 0.11, s * 0.3, 650, accent(t),
                          anchor='middle', letter_spacing=s * 0.012, opacity=0.68)
        span = s * 1.9
        d.append(f'<style>.sheen{uid}{{animation:sheen{uid} 7s ease-in-out {delay:.2f}s infinite}}'
                 f'@keyframes sheen{uid}{{0%{{transform:translateX(0)}}32%,100%{{transform:translateX({span:.0f}px)}}}}</style>')
        body = (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r:.1f}" fill="url(#t{uid})"/>{letters}'
                f'<g clip-path="url(#f{uid})"><rect class="sheen{uid}" x="{x - s * 0.7:.1f}" y="{y}" width="{s * 0.55:.1f}" height="{s}" '
                f'fill="url(#s{uid})"/></g>')
    body += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r:.1f}" fill="none" stroke="{edge}" stroke-width="1.5"/>'
    return ''.join(d), body


def face_svg(t: Theme, p: Person) -> str:
    """Stand-alone portrait for a faculty card."""
    s = 280
    defs = GlyphDefs(prefix='f')
    d, body = portrait(t, p, 2, 2, s, 'F', defs, 0.0)
    return svg_doc(s + 4, s + 4, str(p['name']), body, defs, d)


def member_card(t: Theme, p: Person, idx: int, group_role: str) -> str:
    """Portrait, name, "PhD · 2024" line and projects; shown at 170 px wide in the grid."""
    W, H, S = 340, 424, 272
    defs = GlyphDefs(prefix='c')
    ax = (W - S) / 2
    d, body = portrait(t, p, ax, 6, S, 'M', defs, (idx * 0.55) % 7)
    g = [body]
    name = str(p['name'])
    if p.get('name_zh') and measure(f'{name} · {p["name_zh"]}', 30, 700) <= W - 24:
        name = f'{name} · {p["name_zh"]}'
    s, _ = text(defs, name, W / 2, 6 + S + 54, fit(name, 30, 700, W - 24, 22), 700, t.ink, anchor='middle')
    g.append(s)
    y = 6 + S + 94
    # The section already names the role, so the line only appears once a year (or a title) is known.
    if p.get('year') or p.get('title'):
        role = ' · '.join(str(v) for v in (p.get('title') or group_role, p.get('year')) if v)
        s, _ = text(defs, role, W / 2, y, 23, 500, t.muted, anchor='middle')
        g.append(s)
        y += 32
    works = [str(w) for w in p.get('works') or []]  # type: ignore[union-attr]
    one = ' · '.join(works)
    if not works:
        lines: list[str] = []
    elif measure(one, 21, 600) <= W - 20 or len(works) == 1:
        lines = [one]
    elif y < 6 + S + 120:  # room for two lines
        lines = works[:2]
    else:
        lines = works[:1]
    for line in lines:
        s, _ = text(defs, line, W / 2, y, fit(line, 21, 600, W - 20, 17), 600, accent(t), anchor='middle', opacity=0.9)
        g.append(s)
        y += 29
    return svg_doc(W, H, str(p['name']), ''.join(g), defs, d)


def section_svg(t: Theme, title: str) -> str:
    """Small uppercase label after four loop-coloured squares, then a fading rule (zjureal.com style)."""
    W, H = 1600, 60
    defs = GlyphDefs(prefix='s')
    en, _, zh = title.partition(' · ')
    css = ('<style>.sq{transform-box:fill-box;transform-origin:center;animation:sq 4s ease-in-out infinite}'
           '@keyframes sq{0%,40%,100%{transform:scale(1);opacity:.8}12%{transform:scale(1.3);opacity:1}}</style>'
           f'<linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{t.border}"/>'
           f'<stop offset="1" stop-color="{t.border}" stop-opacity="0"/></linearGradient>')
    g = [f'<rect class="sq" style="animation-delay:{i}s" x="{3 + i * 24}" y="22" width="16" height="16" rx="4" fill="{t.pillars[k]}"/>'
         for i, (k, _, _) in enumerate(PILLARS)]
    x = 3 + 4 * 24 + 18
    s, w = text(defs, en.upper(), x, 38, 22, 700, t.muted, letter_spacing=3.2)
    g.append(s)
    x += w
    if zh:
        s, w2 = text(defs, f'  ·  {zh}', x, 38, 22, 600, t.muted, letter_spacing=1.5)
        g.append(s)
        x += w2
    g.append(f'<rect x="{x + 28:.1f}" y="29" width="{W - x - 28:.1f}" height="2" fill="url(#rule)"/>')
    return svg_doc(W, H, title, ''.join(g), defs, css)


def hero_svg(t: Theme, data: dict[str, object]) -> str:
    """Title and introduction on the left, the group photo (or a placeholder) on the right."""
    W, H = 1600, 560
    defs = GlyphDefs(prefix='h')
    fx, fy, fw, fh = 892, 82, 624, 351
    photos = [str(f) for f in data.get('group_photos') or []]  # type: ignore[union-attr]
    shadow, alpha = SHADOW[t.name]
    extra = [f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t.bg0}"/>'
             f'<stop offset="1" stop-color="{t.bg1}"/></linearGradient>',
             f'<radialGradient id="glow"><stop offset="0" stop-color="{t.glow}" stop-opacity=".7"/>'
             f'<stop offset="1" stop-color="{t.glow}" stop-opacity="0"/></radialGradient>',
             f'<linearGradient id="wm" gradientUnits="userSpaceOnUse" x1="88" y1="0" x2="420" y2="0">'
             f'<stop offset="0" stop-color="{t.brand[0]}"/><stop offset=".55" stop-color="{t.brand[1]}"/>'
             f'<stop offset="1" stop-color="{t.brand[2]}"/></linearGradient>',
             f'<filter id="lift" x="-10%" y="-10%" width="120%" height="135%"><feDropShadow dx="0" dy="14" stdDeviation="18" '
             f'flood-color="{shadow}" flood-opacity="{alpha}"/></filter>',
             f'<clipPath id="frame"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22"/></clipPath>',
             f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{t.muted}" fill-opacity=".22"/></pattern>',
             ring_gradient(t, 'H')]
    g = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="32" fill="url(#bg)" stroke="{t.border}" stroke-width="2"/>',
         f'<circle class="breathe" cx="{fx + fw / 2}" cy="{fy + fh / 2}" r="330" fill="url(#glow)"/>']
    # left column
    x = 88
    s, w = text(defs, 'ZJU-OMNIAI', x, 124, 20, 700, t.muted, letter_spacing=5)
    g.append(s)
    g.append(f'<circle cx="{x + w + 17:.1f}" cy="117" r="3.4" fill="{t.brand[1]}"/>')
    s, _ = text(defs, '浙江大学', x + w + 34, 124, 21, 600, t.muted, letter_spacing=3)
    g.append(s)
    s, pw = text_baked('People', x - 4, 238, 112, 800, 'url(#wm)', letter_spacing=-3)
    g.append(s)
    s, _ = text(defs, '团队成员', x + pw + 22, 238, 50, 700, t.ink, letter_spacing=4)
    g.append(s)
    y = 306
    for line in wrap(str(data.get('hero_en', '')), 25, 450, fx - x - 76):
        s, _ = text(defs, line, x, y, 25, 450, t.body)
        g.append(s)
        y += 39
    y += 10
    for line in wrap(str(data.get('hero_zh', '')), 23, 500, fx - x - 76):
        s, _ = text(defs, line, x, y, 23, 500, t.body)
        g.append(s)
        y += 37
    # photo frame
    g.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22" fill="{t.card}" filter="url(#lift)"/>')
    n = len(photos)
    if n:
        per, fade = 6.0, 0.9
        T = per * n
        css = []
        for i, f in enumerate(photos):
            a, b, e = i * per / T * 100, (i + 1) * per / T * 100, fade / T * 100
            if n > 1:
                if i == 0:
                    keys = f'0%{{opacity:1}}{b - e:.2f}%{{opacity:1}}{b:.2f}%{{opacity:0}}{100 - e:.2f}%{{opacity:0}}100%{{opacity:1}}'
                else:
                    keys = f'0%,{a - e:.2f}%{{opacity:0}}{a:.2f}%,{b - e:.2f}%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}'
                css.append(f'.ph{i}{{animation:ph{i} {T}s linear infinite}}@keyframes ph{i}{{{keys}}}')
            g.append(f'<image class="ph{i}" href="{jpeg_uri(PHOTOS / f, 1248, 702)}" x="{fx}" y="{fy}" width="{fw}" height="{fh}" '
                     f'preserveAspectRatio="xMidYMid slice" clip-path="url(#frame)"/>')
        extra.append(f'<style>{"".join(css)}</style>')
        steps, cycle = n, T
    else:
        g.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22" fill="url(#dots)"/>')
        cx, cy = fx + fw / 2, fy + fh / 2 - 22
        g.append(loop(t, cx, cy, 104, 24, 52, 19, 'H'))
        s, _ = text(defs, 'Group photo coming soon  ·  团队合影即将更新', cx, fy + fh - 28, 18, 600, t.muted, anchor='middle', letter_spacing=1)
        g.append(s)
        steps, cycle = 4, 8.0  # in step with the four loop nodes
    g.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22" fill="none" stroke="{t.card_border}" stroke-width="1.5"/>')
    # carousel dots: the active one stretches into a pill and steps along
    gap = 22
    x0 = fx + fw / 2 - gap * (steps - 1) / 2
    dy = fy + fh + 40
    for i in range(steps):
        g.append(f'<circle cx="{x0 + i * gap:.1f}" cy="{dy}" r="4.5" fill="{t.muted}" fill-opacity=".35"/>')
    if steps > 1:
        frames = []
        for i in range(steps):
            a, b = i / steps * 100, (i + 1) / steps * 100
            frames.append(f'{a + (0.6 if i else 0):.2f}%,{b - 0.6:.2f}%{{transform:translateX({i * gap}px)}}')
        frames.append(f'100%{{transform:translateX(0)}}')
        extra.append(f'<style>.act{{animation:act {cycle}s ease-in-out infinite}}@keyframes act{{{"".join(frames)}}}</style>')
    g.append(f'<rect class="act" x="{x0 - 12:.1f}" y="{dy - 4.5}" width="24" height="9" rx="4.5" fill="{accent(t)}"/>')
    return svg_doc(W, H, 'ZJU-OmniAI People · 团队成员', ''.join(g), defs, ''.join(extra))


# ---------------------------------------------------------------- markdown

def picture(path: str, alt: str, attrs: str) -> str:
    """Light/dark pair; `path` is relative to people/ and ends before -light.svg / -dark.svg."""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{path}-dark.svg">'
            f'<img alt="{html.escape(alt)}" src="{path}-light.svg" {attrs}></picture>')


def link_of(p: Person, key: str) -> str:
    val = str(p[key])
    return {'github': f'https://github.com/{val}', 'x': f'https://x.com/{val}', 'email': f'mailto:{val}'}.get(key, val)


def primary_link(p: Person) -> str:
    for key in ('homepage', 'github', 'scholar'):
        if p.get(key):
            return link_of(p, key)
    return ''


def icons(p: Person, size: int = 18) -> str:
    out = [f'<a href="{html.escape(link_of(p, k))}" title="{ICON_TITLES[k]}"><img src="../profile/assets/icons/{k}.svg" '
           f'alt="{ICON_TITLES[k]}" width="{size}" height="{size}"></a>' for k in ICON_PATHS if p.get(k)]
    return '&nbsp;&nbsp;'.join(out)


def faculty_cell(p: Person, width: int) -> str:
    sl = slug(str(p['name']))
    name = html.escape(str(p['name']))
    if p.get('homepage'):
        name = f'<a href="{html.escape(str(p["homepage"]))}">{name}</a>'
    zh = f' · {html.escape(str(p["name_zh"]))}' if p.get('name_zh') else ''
    lines = [picture(f'assets/faces/{sl}', str(p['name']), 'align="left" width="112"'),
             f'<b>{name}{zh}</b><br>',
             f'<sub>{html.escape(" · ".join(str(v) for v in (p.get("title") or "Faculty", "Zhejiang University")))}</sub><br>']
    if p.get('research'):
        lines.append(f'<sub>{html.escape(str(p["research"]))}</sub><br>')
    if p.get('email'):
        lines.append(f'<sub>{html.escape(str(p["email"]).replace("@", " [AT] "))}</sub><br>')
    lines.append(icons(p))
    lines.append('<br><img src="../profile/assets/spacer.svg" alt="" width="250" height="1">')
    return f'<td valign="top" width="{width}%">\n' + '\n'.join(lines) + '\n</td>'


def member_link(p: Person) -> str:
    sl = slug(str(p['name']))
    alt = str(p['name']) + (f' ({p["name_zh"]})' if p.get('name_zh') else '')
    pic = picture(f'assets/cards/{sl}', alt, 'width="170"')
    href = primary_link(p)
    return f'<a href="{html.escape(href)}" title="{html.escape(alt)}">{pic}</a>' if href else pic


def build(data: dict[str, object]) -> str:
    home = picture('../profile/assets/links/home', 'Homepage', PILL)
    nav = [f'<a href="{ORG}">{home}</a>',
           f'<a href="{ORG}#news">{picture("../profile/assets/links/news", "News", PILL)}</a>',
           f'<a href="https://github.com/orgs/ZJU-OmniAI/repositories">{picture("../profile/assets/links/repos", "All Repositories", PILL)}</a>',
           f'<a href="https://huggingface.co/OmniAI-ZJU">{picture("../profile/assets/links/huggingface", "Hugging Face", PILL)}</a>']
    hero_alt = f'ZJU-OmniAI People. {data.get("hero_en", "")} {data.get("hero_zh", "")}'
    out = ['<!-- Generated by tools/build_people.py from people/people.json. Do not edit by hand. -->', '',
           '<p align="right">', '&nbsp;\n'.join(nav), '</p>', '',
           f'<p>{picture("assets/hero", hero_alt, FULL)}</p>', '']
    if data.get('note'):
        out += [f'<p align="right"><sub>{html.escape(str(data["note"]))}</sub></p>', '']
    for group in data.get('groups') or []:  # type: ignore[union-attr]
        members = group.get('members') or []
        if not members:
            continue
        title = str(group['title'])
        out += [f'<p>{picture("assets/section-" + section_slug(title), title, FULL)}</p>', '']
        if group.get('featured'):
            w = 100 // len(members)
            out += ['<table>', '<tr>', '\n'.join(faculty_cell(m, w) for m in members), '</tr>', '</table>', '']
        else:
            out += ['<p>', '\n'.join(member_link(m) for m in members), '</p>', '']
    alumni = data.get('alumni') or []
    if alumni:
        rows = ''.join(
            f'<tr><td>{html.escape(a["name"])}{" · " + html.escape(a["name_zh"]) if a.get("name_zh") else ""}</td>'
            f'<td>{html.escape(a.get("degree", ""))}</td><td>{html.escape(a.get("now", ""))}</td></tr>' for a in alumni)  # type: ignore[union-attr]
        out += [f'<p>{picture("assets/section-alumni", "Alumni · 毕业生", FULL)}</p>', '',
                f'<table><tr><th align="left">Name</th><th align="left">Degree</th><th align="left">Now</th></tr>{rows}</table>', '']
    out += [picture('../profile/assets/divider', '', FULL), '', '<div align="center">', '<br>',
            '&nbsp;\n'.join(nav + [f'<a href="mailto:{data.get("contact", "")}">'
                                   f'{picture("../profile/assets/links/contact", "Contact", PILL)}</a>']),
            '</div>', '']
    return '\n'.join(out)


def main() -> None:
    data = json.loads((PEOPLE / 'people.json').read_text())
    write_icons()
    for sub in ('cards', 'faces'):
        shutil.rmtree(ASSETS / sub, ignore_errors=True)
        (ASSETS / sub).mkdir(parents=True)
    for old in ASSETS.glob('section-*.svg'):
        old.unlink()
    for t in THEMES:
        (ASSETS / f'hero-{t.name}.svg').write_text(hero_svg(t, data))
        for group in data.get('groups') or []:
            if not group.get('members'):
                continue
            (ASSETS / f'section-{section_slug(str(group["title"]))}-{t.name}.svg').write_text(section_svg(t, str(group['title'])))
            for i, p in enumerate(group['members']):
                sl = slug(str(p['name']))
                if group.get('featured'):
                    (ASSETS / 'faces' / f'{sl}-{t.name}.svg').write_text(face_svg(t, p))
                else:
                    (ASSETS / 'cards' / f'{sl}-{t.name}.svg').write_text(member_card(t, p, i, str(group.get('role', ''))))
        if data.get('alumni'):
            (ASSETS / f'section-alumni-{t.name}.svg').write_text(section_svg(t, 'Alumni · 毕业生'))
    (PEOPLE / 'README.md').write_text(build(data))
    files = sorted(ASSETS.rglob('*.svg'))
    print('wrote people/README.md and', len(files), 'SVGs,', f'{sum(f.stat().st_size for f in files) // 1024} KB total')


if __name__ == '__main__':
    main()
