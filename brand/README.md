# Ionos SDR brand assets

Generator for the organization hero banner and the per-repository social cards.

- `brand_logo.py`: wordmark renderer (sun, halftone band, rounded lettering).
- `make_cards.py`: cards with an optional 3D PCB render under the wordmark. The KiCad render background is keyed out automatically.
- `build_all.py`: regenerates all of the outputs below from sibling working copies.

| Output | Content |
|---|---|
| `profile/img/hero.png` | IonosSDR wordmark with the ionos-sdr-mini rev-B3 render |
| `ionos-sdr-mini/docs/img/social_card.png` | IonosSDR mini with the rev-B3 render |
| `ionos-maximus-rpi-sdr/docs/img/social_card.png`, `banner.png` | IonosSDR maximus, wordmark only (no PCB yet) |

```
pip install pillow numpy
set IONOS_FONT=path\to\NotoSansCJK-Black.ttc   (Windows; on Linux the default path is used)
python build_all.py C:\path\to\GitHub
```

Font: Noto Sans CJK Black (SIL OFL 1.1), from https://github.com/notofonts/noto-cjk.

GitHub does not take the social preview from the repository. Upload each `social_card.png` once under Settings → General → Social preview.
