#!/usr/bin/env python3
"""Stamp the ZJU-OmniAI Lab watermark on cover frames and encode looping WebP.

    python3 tools/watermark_covers.py FRAME_DIR OUT.webp

FRAME_DIR holds the clip as 640x360 PNG frames at 12 fps (cut with ffmpeg).
Three layers, so neither cropping nor patching one spot removes the mark:
  * a slanted, staggered grid of small translucent marks over the whole frame
    that slides diagonally by exactly one lattice step per clip;
  * two larger translucent marks drifting on different closed paths;
  * a fixed badge (ring logo + "ZJU-OmniAI Lab") in the bottom-right corner.
Every motion completes a whole period per clip, so the loop stays seamless.
Requires img2webp (libwebp) on PATH.
"""
from __future__ import annotations

import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

TEXT = 'ZJU-OmniAI Lab'
RING = ((5, 73, 160), (92, 192, 250))
# Verdana Bold keeps the dot on the i of OmniAI legible after WebP compression at small sizes.
FONT_PATHS = ['/System/Library/Fonts/Supplemental/Verdana Bold.ttf', '/System/Library/Fonts/Helvetica.ttc']


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size, index=1) if path.endswith('.ttc') else ImageFont.truetype(path, size)
        except OSError:
            continue
    raise SystemExit('No bold system font found')


def ring_logo(d: int) -> Image.Image:
    """The OmniAI ring: a thick circle with the brand gradient, drawn at 4x then reduced."""
    s = d * 4
    grad = Image.new('RGB', (s, s))
    gp = grad.load()
    for y in range(s):
        for x in range(s):
            t = (x + (s - y)) / (2 * s)
            gp[x, y] = tuple(int(RING[0][c] + (RING[1][c] - RING[0][c]) * t) for c in range(3))  # type: ignore[index]
    mask = Image.new('L', (s, s), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, s - 1, s - 1), fill=255)
    w = int(s * 0.2)
    md.ellipse((w, w, s - 1 - w, s - 1 - w), fill=0)
    out = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out.resize((d, d), Image.LANCZOS)


def badge(height: int, alpha: int, plate: bool) -> Image.Image:
    """Logo + text on one line; optional dark rounded plate behind it."""
    f = font(int(height * 0.46))
    logo = ring_logo(int(height * 0.68))
    tw = int(f.getlength(TEXT))
    pad = int(height * 0.32)
    w = pad + logo.width + int(height * 0.22) + tw + pad
    im = Image.new('RGBA', (w, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if plate:
        d.rounded_rectangle((0, 0, w - 1, height - 1), radius=height // 2, fill=(8, 14, 28, 150))
    im.alpha_composite(logo, (pad, (height - logo.height) // 2))
    tx = pad + logo.width + int(height * 0.22)
    ty = height // 2
    if not plate:  # soft dark halo keeps the floating mark readable on bright footage
        halo = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(halo).text((tx, ty), TEXT, font=f, fill=(0, 0, 0, 170), anchor='lm')
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(2)))
    d.text((tx, ty), TEXT, font=f, fill=(255, 255, 255, 255), anchor='lm')
    if alpha < 255:
        a = im.getchannel('A').point(lambda v: v * alpha // 255)
        im.putalpha(a)
    return im


TILE_DX, TILE_ROW = 230, 92  # staggered lattice: rows shift by TILE_DX/2


def tile_layer(W: int, H: int) -> tuple[Image.Image, int]:
    """Staggered grid of slanted marks, with a margin so any lattice offset can be cropped."""
    mark = badge(20, 80, plate=False).rotate(16, expand=True, resample=Image.BICUBIC)
    margin = TILE_DX + mark.width
    layer = Image.new('RGBA', (W + 2 * margin, H + 2 * margin), (0, 0, 0, 0))
    rows = layer.height // TILE_ROW + 2
    cols = layer.width // TILE_DX + 2
    for r in range(rows):
        shift = TILE_DX // 2 if r % 2 else 0
        for c in range(cols):
            x, y = c * TILE_DX + shift, r * TILE_ROW
            if x + mark.width <= layer.width and y + mark.height <= layer.height:
                layer.alpha_composite(mark, (x, y))
    return layer, margin


def stamp(frames: list[Path], out_dir: Path) -> None:
    corner = badge(28, 235, plate=True)
    drift_a = badge(30, 120, plate=False)
    drift_b = badge(24, 110, plate=False)
    n = len(frames)
    W, H = Image.open(frames[0]).size
    tiles, margin = tile_layer(W, H)
    for i, fp in enumerate(frames):
        im = Image.open(fp).convert('RGBA')
        k = i / n
        # one lattice step (TILE_DX/2, TILE_ROW) per clip maps the grid onto itself
        ox, oy = margin - int(TILE_DX / 2 * k), margin - int(TILE_ROW * k)
        im.alpha_composite(tiles.crop((ox, oy, ox + W, oy + H)))
        phase = 2 * math.pi * k
        for mark, fx, fy, px, py in ((drift_a, 1, 2, 0.0, 0.6), (drift_b, -1, 3, 2.1, 1.3)):
            x = (W - mark.width) / 2 + (W - mark.width) * 0.42 * math.sin(fx * phase + px)
            y = (H - mark.height) / 2 + (H - mark.height) * 0.38 * math.sin(fy * phase + py)
            im.alpha_composite(mark, (int(x), int(y)))
        im.alpha_composite(corner, (W - corner.width - 10, H - corner.height - 10))
        im.convert('RGB').save(out_dir / fp.name)


def main() -> None:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    frames = sorted(src.glob('*.png'))
    if not frames or shutil.which('img2webp') is None:
        raise SystemExit('Need PNG frames and img2webp')
    with tempfile.TemporaryDirectory() as tmp:
        stamp(frames, Path(tmp))
        files = sorted(str(p) for p in Path(tmp).glob('*.png'))
        subprocess.run(['img2webp', '-loop', '0', '-lossy', '-q', sys.argv[3] if len(sys.argv) > 3 else '62', '-m', '4', '-d', '83', *files, '-o', str(out)],
                       check=True, capture_output=True)
    print(f'{out.name}: {len(frames)} frames, {out.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
