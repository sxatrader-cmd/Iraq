#!/usr/bin/env python3
"""Convert Saif's Nippur JPEGs into site webp + OG image. No credit lines.

Looks for the two attachment hashes first, then /tmp/nippur_src copies.
- nippur-ziggurat.webp  = wide ziggurat mound (card / first gallery / OG source)
- nippur-ruins.webp     = tall ziggurat-with-brick-structure shot
- img/og/nippur.jpg     = 1200x630 crop from the wide mound shot

If only one source is present, writes ziggurat + OG and leaves ruins for a later run.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ATTACH = Path("/home/box/agent-data/agents/4aa3939b-ccd5-464b-bc21-3cbaa99162b6/attachments")
TMP = Path("/tmp/nippur_src")

# (preferred path, fallback copies, output webp or None for OG-only)
WIDE_CANDIDATES = [
    ATTACH / "f08ec79a862760b8391810de777d6259e84ce0d3cf28fa34ebcfa1a3938af235.jpg",
    ATTACH / "5539f8912143cc7e67f4d026d170d81ec92323611b7f3eb52732ba0647e991c1.jpg",
    TMP / "saif_nippur.jpg",
]
TALL_CANDIDATES = [
    ATTACH / "04eacbf3335494a37e97ceead887f91adc7b08e14b9ddeea940e1ed6714e85c1.jpg",
    ATTACH / "42fe8d416bdda6792630fe0cfbff8cd3892e2e735f49c54f26828313201c1a92.jpg",
    TMP / "saif_nippur_2.jpg",
]

OUT_WIDE = ROOT / "img" / "nippur-ziggurat.webp"
OUT_TALL = ROOT / "img" / "nippur-ruins.webp"
OG = ROOT / "img" / "og" / "nippur.jpg"


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def load(p: Path) -> Image.Image:
    im = Image.open(p)
    if im.mode != "RGB":
        im = im.convert("RGB")
    return im


def to_webp(im: Image.Image, dest: Path, max_edge=1600, quality=82):
    w, h = im.size
    scale = min(1.0, max_edge / max(w, h))
    out = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS) if scale < 1 else im.copy()
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "WEBP", quality=quality, method=6)
    print(dest.relative_to(ROOT), out.size, dest.stat().st_size)


def to_og(im: Image.Image, dest: Path, size=(1200, 630)):
    tw, th = size
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale + 0.5), int(h * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = max(0, int((nh - th) * 0.25))
    if top + th > nh:
        top = max(0, nh - th)
    im = im.crop((left, top, left + tw, top + th))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=86, optimize=True)
    print(dest.relative_to(ROOT), im.size, dest.stat().st_size)


def main():
    wide = first_existing(WIDE_CANDIDATES)
    tall = first_existing(TALL_CANDIDATES)
    if not wide and not tall:
        raise SystemExit("No Nippur source photos found.")
    if wide:
        print("wide:", wide)
        im = load(wide)
        to_webp(im, OUT_WIDE)
        to_og(im, OG)
    else:
        print("wide shot missing; OG/card will wait")
    if tall:
        print("tall:", tall)
        to_webp(load(tall), OUT_TALL)
    else:
        print("tall shot not found yet; nippur-ruins.webp not written")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
