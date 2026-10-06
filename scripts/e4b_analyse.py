#!/usr/bin/env python3
"""E4b — what in the 'print' layer does the work: the colour cast, the dots, the rephotograph?

Per variant and model: rank of the work's own museum image among the 18 405 (median, share in
the top 10), drift from the original, and (CLIP, SigLIP) the object type read zero-shot.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from impressions import CACHE
import numpy as np

from impressions.corpus import load_works
from impressions.encoders import Encoder
from impressions.gallery import Gallery

KINDS = {"painting": "a painting", "print": "a print, an engraving", "drawing": "a drawing",
         "sculpture": "a sculpture", "photograph": "an old photograph"}


def norm(v):
    return v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-8)


def main() -> None:
    works = {w["id"]: w for w in load_works()}
    rng = np.random.default_rng(0)
    out = {}
    for model in ["clip", "siglip", "dinov2"]:
        gal = Gallery(model)
        # the original = the work's own pool image (same image, already encoded)
        orig = {w: gal.vecs[gal.index[w]] for w in works}
        sc = np.load(f"{CACHE}/screens-{model}.npz")
        V = norm(sc["vecs"].astype(np.float32))
        tk = None
        if model != "dinov2":
            enc = Encoder(model)
            tk = enc.texts([f"a photo of {KINDS[k]}" for k in KINDS])
        res = {}
        rows = [("orig", w, v) for w, v in orig.items()] + list(zip(sc["chain"], sc["work"], V))
        for chain, w, v in rows:
            r = res.setdefault(chain, {"rank": [], "drift": [], "kind": [], "kind_ok": []})
            sims = gal.vecs @ v
            r["rank"].append(int((sims > sims[gal.index[w]]).sum()) + 1)
            r["drift"].append(1 - float(v @ orig[w]))
            if tk is not None:
                g = list(KINDS)[int(np.argmax(tk @ v))]
                r["kind"].append(g)
                r["kind_ok"].append(g == works[w]["kind"])
        summary = {}
        for chain, r in res.items():
            ranks = np.array(r["rank"])
            boot = [np.mean(rng.choice(ranks <= 10, len(ranks))) for _ in range(1000)]
            summary[chain] = {
                "median_rank": float(np.median(ranks)),
                "top10": float(np.mean(ranks <= 10)),
                "top10_ci": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
                "drift": float(np.mean(r["drift"])),
            }
            if r["kind"]:
                summary[chain]["kind_ok"] = float(np.mean(r["kind_ok"]))
                summary[chain]["kinds"] = dict(Counter(r["kind"]))
        out[model] = summary
        print(model)
        for chain, s in summary.items():
            print(f"  {chain:16s} rang médian {s['median_rank']:7.1f}  top10 {s['top10']:.2f} "
                  f"dérive {s['drift']:.3f}  type {s.get('kind_ok', float('nan')):.2f} "
                  f"{s.get('kinds', '')}")
    # screen period once the image (long side 960, completed to a square) is resized to the
    # 224-px input: below ~2 px the dots alias into moiré (review I3)
    out["screen_period_input_px"] = {"ht_cmyk_fine": 3 * 224 / 960, "ht_cmyk_medium": 5 * 224 / 960,
                                     "ht_cmyk_coarse": 8 * 224 / 960, "ht_cmy": 5 * 224 / 960}
    Path("results/E4b").mkdir(parents=True, exist_ok=True)
    json.dump(out, open(f"results/E4b/screens-{CACHE.name}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
