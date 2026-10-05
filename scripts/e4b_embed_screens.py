#!/usr/bin/env python3
"""E4b — encode the screen variants (colour only, CMYK fine/medium/coarse, old CMY, rephoto
only) for the 300 works. Same seeds scheme as E4; resumable per work.
Output: data/cache/screens-<model>.npz (work, chain, vecs)."""

from __future__ import annotations

import json
import sys
import time
import zlib
from pathlib import Path

import numpy as np
from PIL import Image

from impressions.chains import CHAINS
from impressions.corpus import load_works
from impressions.encoders import Encoder
from impressions.layers import apply_chain

VARIANTS = ["ht_cmy", "ht_cmy_colour", "ht_cmyk_fine", "ht_cmyk_medium", "ht_cmyk_coarse",
            "rephoto_only"]


def main(models: list[str]) -> None:
    works = load_works()
    dirs = {m: Path(f"data/cache/screens/{m}") for m in models}
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    encs = {m: Encoder(m) for m in models}
    t0 = time.time()
    for i, w in enumerate(works):
        key = w["id"].replace(":", "_")
        if all((d / f"{key}.npy").exists() for d in dirs.values()):
            continue
        im = Image.open(w["image_abspath"]).convert("RGB")
        ims = [apply_chain(im, CHAINS[v], zlib.crc32(f"{w['id']}|{v}".encode()))[1]
               for v in VARIANTS]
        for m, enc in encs.items():
            np.save(dirs[m] / f"{key}.npy", enc.images(ims, batch=len(ims)).astype(np.float16))
        if i % 20 == 0:
            print(i, f"{time.time() - t0:.0f}s", flush=True)
    for m in models:
        ids = [w["id"] for w in works]
        vecs = np.concatenate([np.load(dirs[m] / f"{i.replace(':', '_')}.npy") for i in ids])
        np.savez(f"data/cache/screens-{m}.npz",
                 work=np.repeat(np.array(ids), len(VARIANTS)),
                 chain=np.tile(np.array(VARIANTS), len(ids)), vecs=vecs)
    print("done")


if __name__ == "__main__":
    main(sys.argv[1:] or ["clip", "siglip", "dinov2"])
