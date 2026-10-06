#!/usr/bin/env python3
"""E4, step 1 — build every stage of every chain for the 300 works and encode them.

Stages are encoded straight from memory (not saved as files, except a few for sheets).
Output: data/cache/stages-<model>.npz with arrays work, chain, k, vecs.
"""

from __future__ import annotations

import sys
import time
import zlib

from punctured_sky import CACHE
import numpy as np
from PIL import Image

from punctured_sky.chains import E4_CHAINS as CHAINS
from punctured_sky.corpus import load_works
from punctured_sky.encoders import Encoder
from punctured_sky.layers import (apply_chain, area_matched, clutter_matched, content_mask,
                                 degraded_matched)


_BACKGROUNDS: list[str] = []


def backgrounds() -> list[str]:
    """Busy pictures that are not supports, for the clutter control: pool paintings."""
    if not _BACKGROUNDS:
        from punctured_sky.corpus import load_pool

        _BACKGROUNDS.extend(sorted(r["image_abspath"] for r in load_pool()
                                   if r["kind"] == "painting"))
    return _BACKGROUNDS


def stages_of(w):
    """Every stage of every chain, each followed by three controls (review B3, I6):
    'match|' the work alone on grey at the same area; 'degr|' the stage itself with every
    non-work pixel greyed (same degradation, no support); 'clut|' the work at the same area
    on a busy painting that is not a support."""
    import random

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
                if name.startswith("ctrl"):
                    continue
                yield f"match|{name}", k, area, area_matched(im, st.size, area)
                yield f"degr|{name}", k, area, degraded_matched(st, mask)
                bg = random.Random(seed + k).choice(backgrounds())
                yield f"clut|{name}", k, area, clutter_matched(im, st.size, area,
                                                               Image.open(bg))


def main(models: list[str]) -> None:
    """Resumable: each work's stages are saved under data/cache/stages/<model>/ as they come."""
    import json
    from pathlib import Path

    works = load_works()
    dirs = {m: Path(f"{CACHE}/stages/{m}") for m in models}
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
        ((CACHE / "stages") / f"{key}.json").write_text(json.dumps(meta))
        if i % 10 == 0:
            print(i, f"{time.time() - t0:.0f}s", flush=True)
    for m in models:
        meta, vecs = [], []
        for w in works:
            key = w["id"].replace(":", "_")
            meta += json.loads(((CACHE / "stages") / f"{key}.json").read_text())
            vecs.append(np.load(dirs[m] / f"{key}.npy"))
        np.savez(f"{CACHE}/stages-{m}.npz", work=np.array([a for a, *_ in meta]),
                 chain=np.array([b for _, b, *_ in meta]),
                 k=np.array([c for _, _, c, _ in meta]),
                 area=np.array([d for *_, d in meta]), vecs=np.concatenate(vecs))
    print("done", len(meta))


if __name__ == "__main__":
    main(sys.argv[1:] or ["clip", "siglip", "dinov2"])
