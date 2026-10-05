#!/usr/bin/env python3
"""E4, step 1 — build every stage of every chain for the 300 works and encode them.

Stages are encoded straight from memory (not saved as files, except a few for sheets).
Output: data/cache/stages-<model>.npz with arrays work, chain, k, vecs.
"""

from __future__ import annotations

import sys
import time
import zlib

import numpy as np
from PIL import Image

from impressions.chains import CHAINS
from impressions.corpus import load_works
from impressions.encoders import Encoder
from impressions.layers import apply_chain


def stages_of(w):
    im = Image.open(w["image_abspath"])
    yield "orig", 0, apply_chain(im, [], 0)[0]
    for name, chain in CHAINS.items():
        seed = zlib.crc32(f"{w['id']}|{name}".encode())
        for k, st in enumerate(apply_chain(im, chain, seed)):
            if k:
                yield name, k, st


def main(models: list[str]) -> None:
    works = load_works()
    encs = {m: Encoder(m) for m in models}
    meta, vecs = [], {m: [] for m in models}
    t0 = time.time()
    for i, w in enumerate(works):
        batch = list(stages_of(w))
        ims = [st for *_, st in batch]
        for m, enc in encs.items():
            vecs[m].append(enc.images(ims, batch=len(ims)))
        meta += [(w["id"], name, k) for name, k, _ in batch]
        if i % 20 == 0:
            print(i, f"{time.time() - t0:.0f}s", flush=True)
    for m in models:
        np.savez(f"data/cache/stages-{m}.npz", work=np.array([a for a, _, _ in meta]),
                 chain=np.array([b for _, b, _ in meta]), k=np.array([c for *_, c in meta]),
                 vecs=np.concatenate(vecs[m]).astype(np.float16))
    print("done", len(meta))


if __name__ == "__main__":
    main(sys.argv[1:] or ["clip", "siglip", "dinov2"])
