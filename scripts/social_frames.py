#!/usr/bin/env python3
"""Social round — cut the real frames out of their photographs (RGBA, transparent outside and in
the opening) and record each opening, so that a frame can be fitted around any content by
nine-slice scaling (corners and ornaments kept, only the mouldings stretched)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

SRC = Path("data/social/src/hi")
OUT = Path("data/social/frames")


def flood(mask: np.ndarray, seeds: list[tuple[int, int]]) -> np.ndarray:
    lab, _ = ndimage.label(mask)
    ids = {lab[y, x] for y, x in seeds if lab[y, x]}
    return np.isin(lab, list(ids)) if ids else np.zeros_like(mask)


def cut(name: str, bg: str) -> dict:
    im = Image.open(SRC / name).convert("RGBA")
    im.thumbnail((1400, 1400))
    a = np.asarray(im).astype(np.int16)
    h, w = a.shape[:2]
    lum = a[..., :3].mean(2)
    if bg == "alpha":
        empty = a[..., 3] < 30
    elif bg == "dark":
        empty = lum < 38
    else:  # black frame on a light background: anything not black is empty
        empty = ndimage.binary_opening(lum > 90, iterations=2)
    corners = [(2, 2), (2, w - 3), (h - 3, 2), (h - 3, w - 3)]
    outside = flood(empty, corners)
    opening = flood(empty & ~outside, [(h // 2, w // 2)])
    ys, xs = np.nonzero(opening)
    box = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    alpha = np.where(outside | opening, 0, 255).astype(np.uint8)
    keep = ndimage.binary_opening(ndimage.binary_closing(alpha > 0, iterations=1), iterations=3)
    lab, n = ndimage.label(keep)  # drop specks not attached to the frame
    if n > 1:
        sizes = ndimage.sum(keep, lab, range(1, n + 1))
        keep = lab == (1 + int(np.argmax(sizes)))
    alpha = keep.astype(np.uint8) * 255
    out = np.asarray(im).copy()
    out[..., 3] = np.minimum(out[..., 3], alpha)
    ys, xs = np.nonzero(out[..., 3] > 0)
    crop = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    fr = Image.fromarray(out).crop(crop)
    ob = [box[0] - crop[0], box[1] - crop[1], box[2] - crop[0], box[3] - crop[1]]
    OUT.mkdir(parents=True, exist_ok=True)
    stem = Path(name).stem
    fr.save(OUT / f"{stem}.png")
    return {"file": f"{stem}.png", "size": fr.size, "opening": ob}


def main() -> None:
    meta = {"frame_classic": cut("frame_classic.png", "alpha"),
            "frame_rococo": cut("frame_rococo.jpg", "dark"),
            "frame_ebonized": cut("frame_ebonized.jpg", "light")}
    (OUT / "frames.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
