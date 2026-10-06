#!/usr/bin/env python3
"""Encode the whole museum pool (the search gallery) with one model; resumable by chunks."""

from __future__ import annotations

import sys
import time
from pathlib import Path

from punctured_sky import CACHE
import numpy as np
from PIL import Image

from punctured_sky.corpus import load_pool
from punctured_sky.encoders import Encoder

CHUNK = 1024


def load(path: str) -> Image.Image:
    im = Image.open(path)
    im.draft("RGB", (448, 448))  # fast JPEG decode at reduced size
    im = im.convert("RGB")
    im.thumbnail((448, 448))
    return im


def main(model: str) -> None:
    pool = load_pool()
    out_dir = Path(f"{CACHE}/pool-{model}")
    out_dir.mkdir(parents=True, exist_ok=True)
    enc = Encoder(model)
    t0 = time.time()
    for start in range(0, len(pool), CHUNK):
        part = out_dir / f"{start:06d}.npy"
        if part.exists():
            continue
        rows = pool[start:start + CHUNK]
        vecs = enc.images((load(r["image_abspath"]) for r in rows), batch=32)
        np.save(part, vecs.astype(np.float16))
        print(model, start + len(rows), f"{time.time() - t0:.0f}s", flush=True)
    vecs = np.concatenate([np.load(p) for p in sorted(out_dir.glob("*.npy"))])
    np.savez(f"{CACHE}/pool-{model}.npz", ids=np.array([r["id"] for r in pool]), vecs=vecs)
    print("done", model, vecs.shape)


if __name__ == "__main__":
    main(sys.argv[1])
