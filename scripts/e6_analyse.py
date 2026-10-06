#!/usr/bin/env python3
"""E6 — the synthetic findings, checked on 171 real reproductions of 22 works.

Within the real set (each work has 5-9 images, chance of a same-work neighbour ~4 %):
- found: rank of the work's clean reference among the 170 other images;
- same_work@5 and same_support@5 (other works' images sharing the query's support label);
- by support type, by number of layers, by area of the work in the image; and a regression of
  log10(rank) on n_layers and log10(area) to separate layers from size (bootstrap over works).
Zero-shot (CLIP, SigLIP): the object type read, by support type.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from punctured_sky import CACHE
import numpy as np

from punctured_sky.encoders import Encoder

KINDS = {"painting": "a painting", "print": "a print, an engraving", "drawing": "a drawing",
         "sculpture": "a sculpture", "photograph": "an old photograph"}


def main() -> None:
    rows = [json.loads(l) for l in open("data/real/manifest.jsonl")]
    rng = np.random.default_rng(0)
    out = {}
    for model in ["clip", "siglip", "dinov2"]:
        d = np.load(f"{CACHE}/real-{model}.npz")
        V = d["vecs"].astype(np.float32)
        V /= np.linalg.norm(V, axis=1, keepdims=True)
        S = V @ V.T
        np.fill_diagonal(S, -np.inf)
        work = np.array([r["work"] for r in rows])
        sup = np.array([r["support"] for r in rows])
        clean = sup == "clean"
        per = []
        for i, r in enumerate(rows):
            if r["support"] == "clean":
                continue
            order = np.argsort(-S[i])
            rank_of = np.empty(len(rows), int)
            rank_of[order] = np.arange(1, len(rows) + 1)
            # one canonical clean reference per work (review m7: the best of several refs
            # favoured works with many clean images)
            refs = np.where(clean & (work == r["work"]))[0][:1]
            top5 = order[:5]
            per.append({
                "work": r["work"], "support": r["support"], "n_layers": r["n_layers"],
                "area": max(r["work_area"], 0.005), "found": int(rank_of[refs].min()),
                "same_work5": float((work[top5] == r["work"]).mean()),
                "same_support5": float(((work[top5] != r["work"]) &
                                        (sup[top5] == r["support"])).mean()),
            })
        by_sup = defaultdict(list)
        for p in per:
            by_sup[p["support"]].append(p)
        bins = {"0-1": (0, 1), "2": (2, 2), "3": (3, 3), "4+": (4, 99)}
        by_layers = {b: [p for p in per if lo <= p["n_layers"] <= hi] for b, (lo, hi) in bins.items()}

        def summ(ps):
            f = np.array([p["found"] for p in ps])
            return {"n": len(ps), "found_top5": float((f <= 5).mean()),
                    "median_rank": float(np.median(f)),
                    "same_work5": float(np.mean([p["same_work5"] for p in ps])),
                    "same_support5": float(np.mean([p["same_support5"] for p in ps]))}

        # log rank ~ n_layers + log area, bootstrap over works
        works = sorted({p["work"] for p in per})
        X = lambda ps: np.column_stack([np.ones(len(ps)), [p["n_layers"] for p in ps],
                                        np.log10([p["area"] for p in ps])])
        y = lambda ps: np.log10([p["found"] for p in ps])
        coefs = []
        for _ in range(2000):
            pick = rng.choice(works, len(works))
            ps = [p for w in pick for p in per if p["work"] == w]
            coefs.append(np.linalg.lstsq(X(ps), y(ps), rcond=None)[0])
        coefs = np.array(coefs)
        point = np.linalg.lstsq(X(per), y(per), rcond=None)[0]
        res = {"by_support": {s: summ(ps) for s, ps in by_sup.items()},
               "by_layers": {b: summ(ps) for b, ps in by_layers.items() if ps},
               "regression_log10_rank": {
                   "n_layers": [float(point[1]), *np.percentile(coefs[:, 1], [2.5, 97.5]).tolist()],
                   "log10_area": [float(point[2]), *np.percentile(coefs[:, 2], [2.5, 97.5]).tolist()]}}
        if model != "dinov2":
            enc = Encoder(model)
            tk = enc.texts([f"a photo of {KINDS[k]}" for k in KINDS])
            guess = [list(KINDS)[int(np.argmax(tk @ v))] for v in V]
            kt = defaultdict(list)
            for r, g in zip(rows, guess):
                kt[r["support"]].append((g, r["work_kind"]))
            res["type_by_support"] = {
                s: {"ok": float(np.mean([g == k for g, k in v])), "read": dict(Counter(g for g, _ in v))}
                for s, v in kt.items()}
        out[model] = res
    Path("results/E6").mkdir(parents=True, exist_ok=True)
    json.dump(out, open(f"results/E6/real-{CACHE.name}.json", "w"), indent=1)
    for m, res in out.items():
        print("##", m, "régression log10(rang) : couches", np.round(res["regression_log10_rank"]["n_layers"], 3),
              "log10(aire)", np.round(res["regression_log10_rank"]["log10_area"], 3))
        for s, v in res["by_support"].items():
            t = res.get("type_by_support", {}).get(s, {})
            print(f"  {s:17s} n={v['n']:3d} trouvé@5 {v['found_top5']:.2f} rang méd {v['median_rank']:5.1f} "
                  f"même œuvre@5 {v['same_work5']:.2f} même support@5 {v['same_support5']:.2f} "
                  f"type {t.get('ok', float('nan')):.2f} {t.get('read', '')}")
        for b, v in res["by_layers"].items():
            print(f"  couches {b:4s} n={v['n']:3d} trouvé@5 {v['found_top5']:.2f} même support@5 {v['same_support5']:.2f}")


if __name__ == "__main__":
    main()
