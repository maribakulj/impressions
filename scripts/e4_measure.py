#!/usr/bin/env python3
"""E4, step 2 — H1 and H2 from the stage embeddings.

Per stage of each chain, for each model:
- drift: 1 - cos(stage, the museum image as given);
- self_rank: rank of the work's own museum image among the 18 405 pool images;
- subj@10: share of the 10 nearest pool images (same near-duplicate group excluded) whose
  Iconclass prefix (3 characters) is the work's;
- kind@10: share of them of the work's object type;
- each stage against three controls at the same area: the work alone on grey ('match'),
  the stage with every non-work pixel greyed ('degr', same degradation), the work on a busy
  non-support picture ('clut').
95 % confidence intervals by bootstrap over works (2 000 resamples).
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from punctured_sky import CACHE
import numpy as np

from punctured_sky.chains import E4_CHAINS as CHAINS
from punctured_sky.corpus import load_pool, load_works
from punctured_sky.gallery import Gallery


def subject(row) -> str:
    return row["iconclass"][0].split("(")[0][:3]


def boot(values: np.ndarray, rng, n=2000):
    if len(values) == 0:
        return [float("nan")] * 3
    idx = rng.integers(0, len(values), (n, len(values)))
    means = values[idx].mean(1)
    return [float(values.mean()), float(np.percentile(means, 2.5)),
            float(np.percentile(means, 97.5))]


def main(model: str) -> None:
    rng = np.random.default_rng(0)
    works = {w["id"]: w for w in load_works()}
    pool = {r["id"]: r for r in load_pool()}
    gal = Gallery(model)
    data = np.load(f"{CACHE}/stages-{model}.npz")
    W, C, K = data["work"], data["chain"], data["k"]
    V = data["vecs"].astype(np.float32)
    V /= np.linalg.norm(V, axis=1, keepdims=True) + 1e-8
    orig = {w: V[i] for i, (w, c) in enumerate(zip(W, C)) if c == "orig"}
    pool_subj = np.array([subject(r) for r in gal.rows])
    pool_kind = np.array([r["kind"] for r in gal.rows])
    pool_dup = np.array([r["near_duplicate_group"] for r in gal.rows])
    # outermost layer of each stage
    A = data["area"]
    per = defaultdict(lambda: defaultdict(list))
    log_rank = {}
    B = 512  # similarities by blocks of rows: fast, and ~40 MB per block instead of ~1 GB
    for i, (w, c, k) in enumerate(zip(W, C, K)):
        if i % B == 0:
            PS = V[i:i + B] @ gal.vecs.T
        work = works[w]
        s_subj, s_kind = subject(work), work["kind"]
        dup = pool[w]["near_duplicate_group"]
        ps = PS[i % B].copy()
        own = gal.index[w]
        self_rank = int((ps > ps[own]).sum()) + 1
        ps[pool_dup == dup] = -np.inf
        top = np.argpartition(-ps, 10)[:10]
        key = (c, int(k))
        per[key]["drift"].append(1 - float(V[i] @ orig[w]))
        per[key]["area"].append(float(A[i]))
        log_rank[(w, c, int(k))] = np.log10(self_rank)
        per[key]["self_rank"].append(self_rank)
        per[key]["self_top10"].append(float(self_rank <= 10))
        per[key]["subj@10"].append(float((pool_subj[top] == s_subj).mean()))
        per[key]["kind@10"].append(float((pool_kind[top] == s_kind).mean()))
    out = {}
    for key, metrics in sorted(per.items()):
        out[f"{key[0]}|{key[1]}"] = {
            m: boot(np.array(v, float), rng) for m, v in metrics.items() if m != "self_rank"
        } | {"self_rank_median": float(np.median(metrics["self_rank"])),
             "n": len(metrics["drift"])}
    # paired H1 contrasts, per work: frame vs controls, frame vs support change without frame
    def drift_of(chain, k):
        return {w: 1 - float(V[i] @ orig[w]) for i, (w, c, kk) in enumerate(zip(W, C, K))
                if c == chain and kk == k}
    contrasts = {}
    pairs = {
        "gilt_frame - ctrl_shrink": (("frame", 1), ("ctrl_shrink", 1)),
        "mat_border - ctrl_shrink": (("mat", 1), ("ctrl_shrink", 1)),
        "gilt_frame - ctrl_jpeg": (("frame", 1), ("ctrl_jpeg", 1)),
        "gilt_frame - halftone_print": (("frame", 1), ("print", 1)),
        "mat_border - halftone_print": (("mat", 1), ("print", 1)),
        "ctrl_shrink - halftone_print": (("ctrl_shrink", 1), ("print", 1)),
    }
    for name, (a, b) in pairs.items():
        da, db = drift_of(*a), drift_of(*b)
        diff = np.array([da[w] - db[w] for w in da if w in db])
        contrasts[name] = boot(diff, rng) + [float((diff > 0).mean())]
    # the decisive control: each stage against the work alone at the same area, no support
    matched = {}
    for ctrl in ("match", "degr", "clut"):  # same area / same degradation / clutter
        for name, chain in CHAINS.items():
            if name.startswith("ctrl"):
                continue
            for k in range(1, len(chain) + 1):
                diff = np.array([log_rank[(w, name, k)] - log_rank[(w, f"{ctrl}|{name}", k)]
                                 for w in works if (w, f"{ctrl}|{name}", k) in log_rank])
                matched[f"{ctrl}|{name}|{k}"] = boot(diff, rng) + [float((diff > 0).mean())]
    Path("results/E4").mkdir(parents=True, exist_ok=True)
    json.dump({"model": model, "stages": out, "h1_contrasts": contrasts,
               "stage_minus_control_log10_rank": matched},
              open(f"results/E4/{model}.json", "w"), indent=1)
    print(model, "written")


if __name__ == "__main__":
    for m in sys.argv[1:] or ["clip", "siglip", "dinov2"]:
        main(m)
