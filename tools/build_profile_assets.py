#!/usr/bin/env python3
"""Build the light/dark SVG graphics used by profile/README.md.

    INTER_DIR=... NOTO_SC_DIR=... python3 tools/build_profile_assets.py

Outputs go to profile/assets/. Edit the data below (DIRECTIONS, PILLARS, LINKS)
and rerun; never hand-edit the generated SVGs.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from svgtext import GlyphDefs, measure, text, text_baked

OUT = Path(__file__).resolve().parent.parent / 'profile' / 'assets'


@dataclass(frozen=True)
class Theme:
    name: str
    bg0: str
    bg1: str
    border: str
    card: str
    card_border: str
    ink: str
    body: str
    muted: str
    brand: tuple[str, str, str]
    ring: tuple[str, str]
    glow: str
    pillars: dict[str, str]
    directions: tuple[str, ...]


LIGHT = Theme(
    name='light', bg0='#F8FBFF', bg1='#EAF2FD', border='#D9E5F5', card='#FFFFFF', card_border='#DCE6F3',
    ink='#0B2447', body='#38526F', muted='#6A819F', brand=('#0549A0', '#0B6BE0', '#3AAEF4'),
    ring=('#0549A0', '#5CC0FA'), glow='#BFE2FD',
    pillars={'perceive': '#0B8A9A', 'reason': '#1E5FD0', 'remember': '#5B4CC4', 'act': '#1C8754'},
    directions=('#1E5FD0', '#5B4CC4', '#0B8A9A', '#1C8754', '#C26A0A', '#B03F7E'),
)
DARK = Theme(
    name='dark', bg0='#0B1322', bg1='#10203A', border='#21365A', card='#111D31', card_border='#24395C',
    ink='#EAF2FF', body='#B7C7DD', muted='#8398B6', brand=('#4C9BFF', '#69C0FF', '#A3E3FF'),
    ring=('#2F7CF0', '#8AD6FF'), glow='#1D4F8F',
    pillars={'perceive': '#2FB8C7', 'reason': '#5E95F6', 'remember': '#9086F2', 'act': '#41BE7E'},
    directions=('#5E95F6', '#9086F2', '#2FB8C7', '#41BE7E', '#E8A23B', '#E07AB2'),
)

# 24-unit stroke icons.
ICONS: dict[str, str] = {
    'perceive': '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3.2"/>',
    'reason': '<path d="M9 18h6M10 21.5h4M12 2.5a6.5 6.5 0 0 0-4 11.6c.8.7 1 1.5 1 2.4V17h6v-.5c0-.9.2-1.7 1-2.4a6.5 6.5 0 0 0-4-11.6Z"/>',
    'remember': '<path d="M12 3 3 7.5 12 12l9-4.5L12 3Z"/><path d="M3 12l9 4.5 9-4.5M3 16.5 12 21l9-4.5"/>',
    'act': '<path d="M3.5 21h10M8.5 21v-3M8.5 18 12 11M12 11l6-3.5M18 7.5l2.6 2.2M18 7.5l.6-3.6"/><circle cx="8.5" cy="18" r="1.7"/><circle cx="12" cy="11" r="1.7"/>',
    'github': '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    'cube': '<path d="M12 2.5 3.5 7v10L12 21.5l8.5-4.5V7L12 2.5Z"/><path d="M3.5 7 12 11.5 20.5 7M12 11.5v10"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    'news': '<path d="M5 4h12v15a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2V5a1 1 0 0 1 1-1Z"/><path d="M17 8h3v11a2 2 0 0 1-2 2M8 8h5M8 12h5M8 16h3"/>',
}

PILLARS: list[tuple[str, str, str]] = [
    ('perceive', 'Perceive', '感知'),
    ('reason', 'Reason', '推理'),
    ('remember', 'Remember', '记忆'),
    ('act', 'Act', '行动'),
]

DIRECTIONS: list[dict[str, object]] = [
    {'no': '01', 'zh': '具身小脑', 'en': 'EMBODIED CEREBELLUM', 'focus': '动作学习 · 高效执行 · 闭环纠错',
     'projects': ['VLA-Corrector', 'VLA-Δ', 'VLA-Rolling']},
    {'no': '02', 'zh': '具身大脑', 'en': 'EMBODIED BRAIN', 'focus': '推理规划 · 具身导航 · 长程记忆',
     'projects': ['Embodied-Reasoner', 'Embodied-Navigator', 'EmbodiedMemory-Bench']},
    {'no': '03', 'zh': '空间智能与世界模型', 'en': 'SPATIAL INTELLIGENCE & WORLD MODELS', 'focus': '交互中学空间 · 空间认知评测 · 3D 场景生成',
     'projects': ['Spatial-Interactor', 'ProVisE', 'Scene-Designer']},
    {'no': '04', 'zh': '可信多模态', 'en': 'TRUSTWORTHY MULTIMODAL', 'focus': '视觉对齐 · 抑制幻觉',
     'projects': ['MGAP', 'OMNEX-VL']},
    {'no': '05', 'zh': '推理与强化学习', 'en': 'REASONING & RL', 'focus': '推理后训练 · 扩散语言模型 RL · 代码生成',
     'projects': ['GFT', 'DTCA', 'VeriRL']},
    {'no': '06', 'zh': '自主智能体', 'en': 'AUTONOMOUS AGENTS', 'focus': '策略自进化 · 工具调用 · 自动工作流',
     'projects': ['Agent-Pro', 'Data-Copilot']},
]

LINKS: list[tuple[str, str, str]] = [
    ('repos', 'github', 'All Repositories'),
    ('huggingface', 'cube', 'Hugging Face'),
    ('news', 'news', 'News'),
    ('contact', 'mail', 'Contact'),
]


def icon(name: str, cx: float, cy: float, size: float, color: str, width: float = 2.0) -> str:
    k = size / 24
    return (f'<g transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({k:.4f})" fill="none" '
            f'stroke="{color}" stroke-width="{width / k:.2f}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def svg_doc(w: int, h: int, title: str, body: str, defs: GlyphDefs, extra_defs: str = '') -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{title}"><title>{title}</title><defs>{extra_defs}{defs.render_defs()}</defs>{body}</svg>\n')


def loop(t: Theme, cx: float, cy: float, orbit: float, node_r: float, ring_r: float, ring_w: float, uid: str) -> str:
    """The perceive -> reason -> remember -> act cycle around the OmniAI ring."""
    out: list[str] = []
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{ring_r}" fill="none" stroke="url(#ring{uid})" stroke-width="{ring_w}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{ring_r - ring_w / 2 + 1.5}" fill="none" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="2"/>')
    angles = [-135, -45, 45, 135]
    keys = [p[0] for p in PILLARS]
    gap = math.degrees(math.asin(min(0.95, (node_r + 10) / orbit)))
    for i, a in enumerate(angles):
        a0, a1 = math.radians(a + gap), math.radians(a + 90 - gap)
        x0, y0 = cx + orbit * math.cos(a0), cy + orbit * math.sin(a0)
        x1, y1 = cx + orbit * math.cos(a1), cy + orbit * math.sin(a1)
        c_from, c_to = t.pillars[keys[i]], t.pillars[keys[(i + 1) % 4]]
        out.append(f'<linearGradient id="arc{uid}{i}" gradientUnits="userSpaceOnUse" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}">'
                   f'<stop offset="0" stop-color="{c_from}"/><stop offset="1" stop-color="{c_to}"/></linearGradient>')
        out.append(f'<path d="M{x0:.1f} {y0:.1f}A{orbit} {orbit} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="url(#arc{uid}{i})" '
                   f'stroke-width="3" stroke-linecap="round" stroke-opacity=".8"/>')
        mid = math.radians(a + 45)
        mx, my = cx + orbit * math.cos(mid), cy + orbit * math.sin(mid)
        tangent = math.degrees(mid) + 90
        out.append(f'<path d="M-7 -7 L5 0 L-7 7" transform="translate({mx:.1f} {my:.1f}) rotate({tangent:.1f})" fill="none" '
                   f'stroke="{c_to}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    for a, key in zip(angles, keys):
        nx, ny = cx + orbit * math.cos(math.radians(a)), cy + orbit * math.sin(math.radians(a))
        color = t.pillars[key]
        out.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r + 7}" fill="{color}" fill-opacity=".12"/>')
        out.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r}" fill="{t.card}" stroke="{color}" stroke-width="3"/>')
        out.append(icon(key, nx, ny, node_r * 1.05, color, 2.2))
    return ''.join(out)


def ring_gradient(t: Theme, uid: str) -> str:
    return (f'<linearGradient id="ring{uid}" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{t.ring[0]}"/>'
            f'<stop offset="1" stop-color="{t.ring[1]}"/></linearGradient>')


def banner(t: Theme) -> str:
    W, H = 1600, 480
    defs = GlyphDefs(prefix='b')
    g: list[str] = []
    extra = (f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t.bg0}"/>'
             f'<stop offset="1" stop-color="{t.bg1}"/></linearGradient>'
             f'<radialGradient id="glow"><stop offset="0" stop-color="{t.glow}" stop-opacity=".75"/>'
             f'<stop offset="1" stop-color="{t.glow}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="wm" gradientUnits="userSpaceOnUse" x1="96" y1="0" x2="620" y2="0">'
             f'<stop offset="0" stop-color="{t.brand[0]}"/><stop offset=".55" stop-color="{t.brand[1]}"/>'
             f'<stop offset="1" stop-color="{t.brand[2]}"/></linearGradient>'
             f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="{t.muted}" fill-opacity=".22"/></pattern>'
             + ring_gradient(t, 'B'))
    g.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="url(#bg)" stroke="{t.border}" stroke-width="2"/>')
    g.append(f'<rect x="1000" y="24" width="576" height="432" fill="url(#dots)"/>')
    g.append('<circle cx="1290" cy="240" r="250" fill="url(#glow)"/>')
    x = 96
    s, w = text(defs, 'ZHEJIANG UNIVERSITY', x, 116, 21, 700, t.muted, letter_spacing=5)
    g.append(s)
    g.append(f'<circle cx="{x + w + 18:.1f}" cy="109" r="3.5" fill="{t.brand[1]}"/>')
    s, _ = text(defs, '浙江大学', x + w + 36, 116, 22, 600, t.muted, letter_spacing=3)
    g.append(s)
    s, _ = text_baked('OmniAI', x - 6, 262, 148, 800, 'url(#wm)', letter_spacing=-4)
    g.append(s)
    s, _ = text(defs, 'Embodied Intelligence & General-Purpose AI', x, 326, 33, 500, t.body)
    g.append(s)
    cx = x
    for i, (key, label, _zh) in enumerate(PILLARS):
        color = t.pillars[key]
        g.append(f'<rect x="{cx}" y="366" width="48" height="48" rx="13" fill="{color}"/>')
        g.append(icon(key, cx + 24, 390, 28, '#FFFFFF', 2.3))
        s, lw = text(defs, label, cx + 62, 399, 26, 700, t.ink)
        g.append(s)
        cx += 62 + lw
        if i < len(PILLARS) - 1:
            g.append(f'<path d="M{cx + 22} 382l8 8-8 8" fill="none" stroke="{t.muted}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
            cx += 52
    g.append(f'<circle cx="1290" cy="240" r="205" fill="none" stroke="{t.border}" stroke-width="1.5" stroke-dasharray="3 9"/>')
    g.append(loop(t, 1290, 240, 160, 36, 84, 30, 'B'))
    return svg_doc(W, H, 'ZJU-OmniAI: Embodied Intelligence and General-Purpose AI. Perceive, reason, remember, act.',
                   ''.join(g), defs, extra)


def chips_layout(names: list[str], size: float, pad: float, gap: float, max_w: float) -> list[list[tuple[str, float]]]:
    rows: list[list[tuple[str, float]]] = [[]]
    used = 0.0
    for n in names:
        w = measure(n, size, 650) + 2 * pad
        if rows[-1] and used + gap + w > max_w:
            rows.append([])
            used = 0.0
        used += (gap if rows[-1] else 0) + w
        rows[-1].append((n, w))
    return rows


def research_map(t: Theme) -> str:
    W, H = 1600, 960
    defs = GlyphDefs(prefix='m')
    g: list[str] = []
    extra = (f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t.bg0}"/>'
             f'<stop offset="1" stop-color="{t.bg1}"/></linearGradient>'
             f'<radialGradient id="glow"><stop offset="0" stop-color="{t.glow}" stop-opacity=".7"/>'
             f'<stop offset="1" stop-color="{t.glow}" stop-opacity="0"/></radialGradient>' + ring_gradient(t, 'M'))
    g.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="url(#bg)" stroke="{t.border}" stroke-width="2"/>')
    cx, cy = 800, 517
    g.append(f'<circle cx="{cx}" cy="{cy}" r="250" fill="url(#glow)"/>')
    col_x = {'L': 40, 'R': 1040}
    card_w, card_h, top, vgap = 520, 262, 104, 20
    heads = [('L', '具身智能', 'EMBODIED INTELLIGENCE', t.directions[0]), ('R', '通用智能', 'GENERAL-PURPOSE AI', t.directions[4])]
    for side, zh, en, color in heads:
        x0 = col_x[side] + 6
        s, w = text(defs, zh, x0, 72, 26, 800, t.ink)
        g.append(s)
        s, _ = text(defs, en, x0 + w + 16, 71, 17, 700, color, letter_spacing=2.6)
        g.append(s)
    outer = 212
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{outer}" fill="none" stroke="{t.border}" stroke-width="2" stroke-dasharray="3 9"/>')
    for i, d in enumerate(DIRECTIONS):
        side = 'L' if i < 3 else 'R'
        row = i % 3
        x0, y0 = col_x[side], top + row * (card_h + vgap)
        color = t.directions[i]
        # connector from card edge to the outer ring
        ymid = y0 + card_h / 2
        ang = math.radians({0: 207, 1: 180, 2: 153}[row] if side == 'L' else {0: -27, 1: 0, 2: 27}[row])
        tx, ty = cx + outer * math.cos(ang), cy + outer * math.sin(ang)
        ex = x0 + card_w if side == 'L' else x0
        mx = (ex + tx) / 2
        g.append(f'<path d="M{ex} {ymid:.1f}C{mx:.1f} {ymid:.1f} {mx:.1f} {ty:.1f} {tx:.1f} {ty:.1f}" fill="none" stroke="{color}" '
                 f'stroke-opacity=".6" stroke-width="2.2" stroke-dasharray="6 6"/>')
        g.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="6" fill="{color}"/>')
        g.append(f'<rect x="{x0}" y="{y0}" width="{card_w}" height="{card_h}" rx="20" fill="{t.card}" stroke="{t.card_border}" stroke-width="1.6"/>')
        g.append(f'<circle cx="{ex}" cy="{ymid:.1f}" r="5" fill="{color}"/>')
        g.append(f'<rect x="{x0}" y="{y0 + 22}" width="5" height="{card_h - 44}" rx="2.5" fill="{color}"/>')
        g.append(f'<rect x="{x0 + 28}" y="{y0 + 26}" width="58" height="36" rx="18" fill="{color}" fill-opacity=".13"/>')
        s, _ = text(defs, str(d['no']), x0 + 57, y0 + 51, 19, 800, color, anchor='middle', letter_spacing=1)
        g.append(s)
        s, _ = text(defs, str(d['zh']), x0 + 102, y0 + 55, 30, 800, t.ink)
        g.append(s)
        s, _ = text(defs, str(d['en']), x0 + 30, y0 + 98, 16, 700, color, letter_spacing=2.2)
        g.append(s)
        s, _ = text(defs, str(d['focus']), x0 + 30, y0 + 134, 21, 500, t.body)
        g.append(s)
        rows = chips_layout(list(d['projects']), 17, 13, 8, card_w - 60)  # type: ignore[arg-type]
        chip_h, chip_gap = 38, 10
        block = len(rows) * chip_h + (len(rows) - 1) * chip_gap
        area_top, area_bottom = y0 + 154, y0 + card_h - 20
        cy0 = round(area_top + (area_bottom - area_top - block) / 2)
        for r_i, r in enumerate(rows):
            px = x0 + 30
            py = cy0 + r_i * (chip_h + chip_gap)
            for name, w in r:
                g.append(f'<rect x="{px:.1f}" y="{py}" width="{w:.1f}" height="{chip_h}" rx="{chip_h / 2}" fill="{color}" '
                         f'fill-opacity=".09" stroke="{color}" stroke-opacity=".38" stroke-width="1.4"/>')
                s, _ = text(defs, name, px + w / 2, py + 25, 17, 650, color, anchor='middle')
                g.append(s)
                px += w + 8
    g.append(loop(t, cx, cy, 150, 32, 70, 24, 'M'))
    for (key, label, zh), a in zip(PILLARS, (-135, -45, 45, 135)):
        nx = cx + 150 * math.cos(math.radians(a))
        ny = cy + 150 * math.sin(math.radians(a))
        above = a < 0
        ly = ny - 54 if above else ny + 74
        s, _ = text(defs, label.upper(), nx, ly, 17, 800, t.pillars[key], anchor='middle', letter_spacing=2)
        g.append(s)
        s, _ = text(defs, zh, nx, ly + (-24 if above else 26), 17, 600, t.muted, anchor='middle', letter_spacing=2)
        g.append(s)
    s, _ = text(defs, '从感知、推理、记忆到行动的智能闭环', cx, 880, 22, 600, t.ink, anchor='middle', letter_spacing=1)
    g.append(s)
    s, _ = text(defs, 'Learning to perceive, reason, remember, and act', cx, 912, 17, 500, t.muted, anchor='middle')
    g.append(s)
    return svg_doc(W, H, 'OmniAI research map: six research directions around the perceive, reason, remember, act loop',
                   ''.join(g), defs, extra)


def divider(t: Theme) -> str:
    W, H = 1200, 28
    colors = [t.pillars[k] for k, _, _ in PILLARS]
    out = [f'<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{t.border}" stop-opacity="0"/><stop offset="1" stop-color="{t.border}"/></linearGradient>',
           f'<linearGradient id="r" x1="0" x2="1"><stop offset="0" stop-color="{t.border}"/><stop offset="1" stop-color="{t.border}" stop-opacity="0"/></linearGradient>']
    body = [f'<rect x="60" y="13" width="486" height="2" fill="url(#l)"/>', f'<rect x="654" y="13" width="486" height="2" fill="url(#r)"/>']
    for i, c in enumerate(colors):
        body.append(f'<circle cx="{573 + i * 18}" cy="14" r="4.4" fill="{c}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">'
            f'<defs>{"".join(out)}</defs>{"".join(body)}</svg>\n')


def pill(t: Theme, icon_name: str, label: str, solid: bool = False) -> str:
    defs = GlyphDefs(prefix='p')
    color = t.brand[0] if t.name == 'light' else t.brand[1]
    lw = measure(label, 13, 650)
    W, H = round(36 + lw + 14), 28
    fg = '#FFFFFF' if solid else color
    bg = (f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{(H - 1.5) / 2}" fill="{color}"/>' if solid else
          f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{(H - 1.5) / 2}" fill="{color}" fill-opacity=".07" '
          f'stroke="{color}" stroke-opacity=".5" stroke-width="1.5"/>')
    s, _ = text(defs, label, 32, 18.6, 13, 650, fg)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
            f'<title>{label}</title><defs>{defs.render_defs()}</defs>{bg}{icon(icon_name, 19, 14, 15, fg, 1.9)}{s}</svg>\n')


def main() -> None:
    (OUT / 'links').mkdir(parents=True, exist_ok=True)
    for t in (LIGHT, DARK):
        (OUT / f'banner-{t.name}.svg').write_text(banner(t))
        (OUT / f'research-map-{t.name}.svg').write_text(research_map(t))
        (OUT / f'divider-{t.name}.svg').write_text(divider(t))
        for slug, ic, label in LINKS:
            (OUT / 'links' / f'{slug}-{t.name}.svg').write_text(pill(t, ic, label, solid=(slug == 'contact')))
    for p in sorted(OUT.rglob('*.svg')):
        print(f'{p.stat().st_size / 1024:7.1f} KB  {p.relative_to(OUT.parent.parent)}')


if __name__ == '__main__':
    main()
