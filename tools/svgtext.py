"""Turn text into SVG outlines so profile graphics render identically everywhere.

GitHub serves README images through its image proxy, so an SVG can only use the
fonts installed on each viewer's machine. Outlining the text removes that
dependency. Glyphs are defined once in <defs> and placed with <use>, which keeps
the files small even with Chinese text.

Fonts (both SIL OFL 1.1) come from Fontsource:
  @fontsource-variable/inter        -> inter-{latin,latin-ext,greek}-wght-normal.woff2
  @fontsource-variable/noto-sans-sc -> noto-sans-sc-*-wght-normal.woff2
Point INTER_DIR and NOTO_SC_DIR at the package `files/` folders.
"""
from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


def _font_files() -> list[str]:
    inter_dir = os.environ.get('INTER_DIR', '')
    noto_dir = os.environ.get('NOTO_SC_DIR', '')
    inter = [os.path.join(inter_dir, f'inter-{s}-wght-normal.woff2') for s in ('latin', 'latin-ext', 'greek')]
    noto = sorted(glob.glob(os.path.join(noto_dir, 'noto-sans-sc-*-wght-normal.woff2')))
    files = [f for f in inter if os.path.exists(f)] + noto
    if len(files) < 4:
        raise SystemExit('Set INTER_DIR and NOTO_SC_DIR to the Fontsource woff2 folders (see module docstring).')
    return files


class FontBook:
    """Lazy per-character font lookup with static instances per weight."""

    def __init__(self) -> None:
        self.files = _font_files()
        self._cmaps: dict[str, dict[int, str]] = {}
        self._instances: dict[tuple[str, int], TTFont] = {}

    def _cmap(self, path: str) -> dict[int, str]:
        if path not in self._cmaps:
            self._cmaps[path] = TTFont(path, lazy=True).getBestCmap() or {}
        return self._cmaps[path]

    def locate(self, ch: str) -> str:
        code = ord(ch)
        for path in self.files:
            if code in self._cmap(path):
                return path
        raise KeyError(f'No font covers {ch!r} (U+{code:04X})')

    def instance(self, path: str, weight: int) -> TTFont:
        key = (path, weight)
        if key not in self._instances:
            font = TTFont(path)
            if 'fvar' in font:
                axis = next(a for a in font['fvar'].axes if a.axisTag == 'wght')
                w = max(axis.minValue, min(axis.maxValue, weight))
                font = instantiateVariableFont(font, {'wght': w})
            self._instances[key] = font
        return self._instances[key]


BOOK: FontBook | None = None


def book() -> FontBook:
    global BOOK
    if BOOK is None:
        BOOK = FontBook()
    return BOOK


@dataclass
class GlyphDefs:
    """Collects glyph outlines used by one SVG document."""

    prefix: str = 'g'
    defs: dict[str, str] = field(default_factory=dict)

    def glyph(self, path: str, weight: int, ch: str) -> tuple[str | None, float, int]:
        """Return (def id or None for blank glyphs, advance in font units, units per em)."""
        font = book().instance(path, weight)
        name = font.getBestCmap()[ord(ch)]
        upem = font['head'].unitsPerEm
        advance = font['hmtx'][name][0]
        file_tag = re.sub(r'[^a-z0-9]', '', os.path.basename(path).replace('-wght-normal.woff2', ''))[-6:]
        gid = f'{self.prefix}{file_tag}{weight}{re.sub(r"[^A-Za-z0-9]", "_", name)}'
        if gid not in self.defs:
            pen = SVGPathPen(font.getGlyphSet(), ntos=lambda v: f'{round(v)}')
            font.getGlyphSet()[name].draw(pen)
            d = pen.getCommands()
            self.defs[gid] = d
        return (gid if self.defs[gid] else None), advance, upem

    def render_defs(self) -> str:
        return ''.join(f'<path id="{k}" d="{v}"/>' for k, v in self.defs.items() if v)


def measure(text: str, size: float, weight: int, letter_spacing: float = 0.0) -> float:
    width = 0.0
    for ch in text:
        path = book().locate(ch)
        font = book().instance(path, weight)
        name = font.getBestCmap()[ord(ch)]
        width += font['hmtx'][name][0] * size / font['head'].unitsPerEm
    return width + letter_spacing * max(0, len(text) - 1)


def text(defs: GlyphDefs, s: str, x: float, y: float, size: float, weight: int = 400,
         fill: str = '#000', anchor: str = 'start', letter_spacing: float = 0.0,
         opacity: float | None = None) -> tuple[str, float]:
    """Outline `s` with its baseline at y. Returns (svg markup, width)."""
    width = measure(s, size, weight, letter_spacing)
    if anchor == 'middle':
        x -= width / 2
    elif anchor == 'end':
        x -= width
    parts: list[str] = []
    cursor = x
    for ch in s:
        path = book().locate(ch)
        gid, adv, upem = defs.glyph(path, weight, ch)
        k = size / upem
        if gid:
            parts.append(f'<use href="#{gid}" transform="translate({cursor:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})"/>')
        cursor += adv * k + letter_spacing
    op = f' opacity="{opacity}"' if opacity is not None else ''
    return f'<g fill="{fill}"{op}>{"".join(parts)}</g>', width


def text_baked(s: str, x: float, y: float, size: float, weight: int, fill: str,
               letter_spacing: float = 0.0) -> tuple[str, float]:
    """Outline with absolute coordinates (needed when one gradient must span the whole word)."""
    cursor = x
    ds: list[str] = []
    for ch in s:
        path = book().locate(ch)
        font = book().instance(path, weight)
        name = font.getBestCmap()[ord(ch)]
        k = size / font['head'].unitsPerEm
        pen = SVGPathPen(font.getGlyphSet(), ntos=lambda v: f'{v:.1f}'.rstrip('0').rstrip('.'))
        font.getGlyphSet()[name].draw(TransformPen(pen, (k, 0, 0, -k, cursor, y)))
        ds.append(pen.getCommands())
        cursor += font['hmtx'][name][0] * k + letter_spacing
    return f'<path fill="{fill}" d="{"".join(ds)}"/>', cursor - letter_spacing - x
