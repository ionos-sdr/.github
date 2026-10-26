#!/usr/bin/env python3
"""Regenerate every Ionos SDR banner and social card.

Run from anywhere: python build_all.py [github_root]
github_root defaults to the parent of this repository and must contain the
ionos-sdr-mini and ionos-maximus-rpi-sdr working copies.
Font: Noto Sans CJK Black; set IONOS_FONT if it is not at the default path.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_cards as C

root = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", ".."))
mini = os.path.join(root, "ionos-sdr-mini")
maxi = os.path.join(root, "ionos-maximus-rpi-sdr")
render = os.path.join(mini, "docs", "img", "ionos-sdr-mini_revB3_2L_3d_iso.jpg")
pcb = C.cutout(render)

prof = os.path.join(HERE, "..", "profile", "img")
os.makedirs(prof, exist_ok=True)
C.card(1600, 800, [("IonosSDR", 190)], 190, pcb).save(os.path.join(prof, "hero.png"), optimize=True)

# ionos-sdr-mini: social card gets the PCB under the wordmark
C.card(1280, 640, [("IonosSDR", 150), ("mini", 96)], 150, pcb).save(
    os.path.join(mini, "docs", "img", "social_card.png"), optimize=True)

# ionos-maximus-rpi-sdr: no PCB yet, wordmark only (card + README banner)
mimg = os.path.join(maxi, "docs", "img"); os.makedirs(mimg, exist_ok=True)
big = [("IonosSDR", 150), ("maximus", 96)]
C.card(1280, 640, big, 150, None).save(os.path.join(mimg, "social_card.png"), optimize=True)
b, _ = C.L.compose(1600, 420, 150, big, sun_pos=(0.10, 0.20), sun_r=0.17, band_pad=0.20)
b.save(os.path.join(mimg, "banner.png"), optimize=True)
print("done")
