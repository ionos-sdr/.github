#!/usr/bin/env python3
"""Ionos SDR social cards and banners with an optional 3D PCB render under the
wordmark. Builds on brand_logo.py (same directory). Pillow + numpy.

Usage: python make_cards.py <outdir> <render.jpg|-> <line1> [line2]
  writes <outdir>/social_card.png (1280x640) and <outdir>/banner.png (1600x420
  wordmark-only README header, unchanged style) unless --card-only is given.

The KiCad render background (vertical gradient) is keyed out by flood fill
from the image border, so bluish parts inside the board (OLED) are kept.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import brand_logo as L

def cutout(path, tol=22):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    # row background from the left and right border columns, interpolated
    left, right = a[:, :4].mean(axis=1), a[:, -4:].mean(axis=1)
    xs = np.linspace(0, 1, w)[None, :, None]
    bg = left[:, None, :] * (1 - xs) + right[:, None, :] * xs
    near = (np.abs(a - bg).max(axis=2) < tol)
    # KiCad soft shadow under the board: same lavender tint, darker
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    near |= (np.abs(r - g) < 8) & (b - r > 12) & (b - r < 40)
    m = Image.fromarray(np.where(near, 255, 0).astype(np.uint8)).copy()
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1)]:
        if m.getpixel(seed) == 255:
            ImageDraw.floodfill(m, seed, 128)
    alpha = Image.fromarray(np.where(np.asarray(m) == 128, 0, 255).astype(np.uint8))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    im.putalpha(alpha)
    return im.crop(alpha.getbbox())

def place_pcb(img, pcb, box):
    """Fit pcb (RGBA) into box (x0, y0, x1, y1), centred, with a warm glow."""
    w, h = img.size
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / pcb.size[0], (by1 - by0) / pcb.size[1])
    p = pcb.resize((int(pcb.size[0] * s), int(pcb.size[1] * s)), Image.LANCZOS)
    px = bx0 + ((bx1 - bx0) - p.size[0]) // 2
    py = by0 + ((by1 - by0) - p.size[1]) // 2
    a = Image.new("L", (w, h), 0); a.paste(p.getchannel("A"), (px, py))
    glow = a.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.55))
    img = ImageChops.screen(img, Image.composite(Image.new("RGB", (w, h), (255, 120, 50)),
                                                 Image.new("RGB", (w, h), (0, 0, 0)), glow))
    shadow = ImageChops.offset(a, 0, 14).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.7))
    img = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), img, shadow)
    img.paste(p, (px, py), p)
    return img

def card(w, h, lines, size, pcb=None, sun_pos=(0.12, 0.20), sun_r=0.15):
    if pcb is None:
        img, _ = L.compose(w, h, size, lines, sun_pos=sun_pos, sun_r=sun_r,
                           band_pad=0.24 if len(lines) > 1 else 0.32)
        return img
    small = [(t, int(s * 0.62)) for t, s in lines]
    img, (y0, y1) = L.compose(w, h, int(size * 0.62), small, sun_pos=(0.07, 0.10), sun_r=0.07,
                              band_pad=0.16, text_cy=0.22)
    margin = int(h * 0.035)
    img = place_pcb(img, pcb, (int(w * 0.04), y1 + margin, int(w * 0.96), h - margin))
    return L.vignette(img)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    card_only = "--card-only" in sys.argv
    out, render, lines = args[0], args[1], args[2:]
    pcb = None if render == "-" else cutout(render)
    big = [(lines[0], 150)] + ([(lines[1], 96)] if len(lines) > 1 else [])
    card(1280, 640, big, 150, pcb).save(f"{out}/social_card.png", optimize=True)
    if not card_only:
        b, _ = L.compose(1600, 420, 150, big, sun_pos=(0.10, 0.20), sun_r=0.17, band_pad=0.20)
        b.save(f"{out}/banner.png", optimize=True)
    print("wrote", out)

if __name__ == "__main__":
    main()
