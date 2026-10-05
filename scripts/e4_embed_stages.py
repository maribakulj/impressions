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
from impressions.layers import apply_chain, area_matched, content_mask


def stages_of(w):
    """Every stage of every chain, each followed by its area-matched control ('match|chain'):
    the work alone on grey, covering the same share of the same canvas, no frame."""
    im = Image.open(w["image_abspath"]).convert("RGB")
    yield "orig", 0, 1.0, apply_chain(im, [], 0)[0]
    for name, chain in CHAINS.items():
        seed = zlib.crc32(f"{w['id']}|{name}".encode())
        stages = apply_chain(im, chain, seed)
        masks = content_mask(stages[0].size, chain, seed)
        for k, (st, mask) in enumerate(zip(stages, masks)):
            if k:
                area = float(mask.mean())
                yield name, k, area, st
                yield f"match|{name}", k, area, area_matched(im, st.size, area)


def main(models: list[str]) -> None:
    """Resumable: each work's stages are saved under data/cache/stages/<model>/ as they come."""
    import json
    from pathlib import Path

    works = load_works()
    dirs = {m: Path(f"data/cache/stages/{m}") for m in models}
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    encs = {m: Encoder(m) for m in models}
    t0 = time.time()
    for i, w in enumerate(works):
        key = w["id"].replace(":", "_")
        if all((d / f"{key}.npy").exists() for d in dirs.values()):
            continue
        batch = list(stages_of(w))
        ims = [st for *_, st in batch]
        for m, enc in encs.items():
            np.save(dirs[m] / f"{key}.npy", enc.images(ims, batch=len(ims)).astype(np.float16))
        meta = [(w["id"], name, k, area) for name, k, area, _ in batch]
        (Path("data/cache/stages") / f"{key}.json").write_text(json.dumps(meta))
        if i % 10 == 0:
            print(i, f"{time.time() - t0:.0f}s", flush=True)
    for m in models:
        meta, vecs = [], []
        for w in works:
            key = w["id"].replace(":", "_")
            meta += json.loads((Path("data/cache/stages") / f"{key}.json").read_text())
            vecs.append(np.load(dirs[m] / f"{key}.npy"))
        np.savez(f"data/cache/stages-{m}.npz", work=np.array([a for a, *_ in meta]),
                 chain=np.array([b for _, b, *_ in meta]),
                 k=np.array([c for _, _, c, _ in meta]),
                 area=np.array([d for *_, d in meta]), vecs=np.concatenate(vecs))
    print("done", len(meta))


if __name__ == "__main__":
    main(sys.argv[1:] or ["clip", "siglip", "dinov2"])
