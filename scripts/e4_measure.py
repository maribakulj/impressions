#!/usr/bin/env python3
"""E4, step 2 — H1 and H2 from the stage embeddings.

Per stage of each chain, for each model:
- drift: 1 - cos(stage, the museum image as given);
- self_rank: rank of the work's own museum image among the 18 405 pool images;
- subj@10: share of the 10 nearest pool images (same near-duplicate group excluded) whose
  Iconclass prefix (3 characters) is the work's;
- kind@10: share of them of the work's object type;
- in a mixed gallery (pool + every stage of the *other* 299 works): same_support@10 = share of
  neighbours that are stages whose outermost layer is the query's, and same_subject@10 = share
  of neighbours (pool or stage) whose Iconclass prefix is the work's.
95 % confidence intervals by bootstrap over works (2 000 resamples).
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from impressions.chains import CHAINS
from impressions.corpus import load_pool, load_works
from impressions.gallery import Gallery


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
    data = np.load(f"data/cache/stages-{model}.npz")
    W, C, K = data["work"], data["chain"], data["k"]
    V = data["vecs"].astype(np.float32)
    V /= np.linalg.norm(V, axis=1, keepdims=True) + 1e-8
    orig = {w: V[i] for i, (w, c) in enumerate(zip(W, C)) if c == "orig"}
    pool_subj = np.array([subject(r) for r in gal.rows])
    pool_kind = np.array([r["kind"] for r in gal.rows])
    pool_dup = np.array([r["near_duplicate_group"] for r in gal.rows])
    # outermost layer of each stage
    last = np.array(["orig" if c == "orig" else "match" if c.startswith("match|")
                     else CHAINS[c][k - 1] for c, k in zip(C, K)])
    A = data["area"]
    stage_subj = np.array([subject(works[w]) for w in W])
    per = defaultdict(lambda: defaultdict(list))
    log_rank = {}
    for i, (w, c, k) in enumerate(zip(W, C, K)):
        work = works[w]
        s_subj, s_kind = subject(work), work["kind"]
        dup = pool[w]["near_duplicate_group"]
        ps = gal.vecs @ V[i]  # row by row: the full matrices would take ~1 GB per model
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
        # mixed gallery: pool (minus duplicates) + stages of other works
        ss = V @ V[i]
        ss[W == w] = -np.inf
        allsims = np.concatenate([ps, ss])
        top = np.argpartition(-allsims, 10)[:10]
        is_stage = top >= len(ps)
        st = top[is_stage] - len(ps)
        same_support = (last[st] == last[i]).sum() if c != "orig" else (last[st] == "orig").sum()
        subj_hits = (pool_subj[top[~is_stage]] == s_subj).sum() + (stage_subj[st] == s_subj).sum()
        per[key]["same_support@10"].append(float(same_support) / 10)
        per[key]["stage_share@10"].append(float(is_stage.mean()))
        per[key]["same_subject_mixed@10"].append(float(subj_hits) / 10)
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
    for name, chain in CHAINS.items():
        if name.startswith(("ctrl", "ht_", "rephoto_only")):
            continue
        for k in range(1, len(chain) + 1):
            diff = np.array([log_rank[(w, name, k)] - log_rank[(w, f"match|{name}", k)]
                             for w in works if (w, name, k) in log_rank])
            matched[f"{name}|{k}"] = boot(diff, rng) + [float((diff > 0).mean())]
    Path("results/E4").mkdir(parents=True, exist_ok=True)
    json.dump({"model": model, "stages": out, "h1_contrasts": contrasts,
               "stage_minus_area_matched_log10_rank": matched},
              open(f"results/E4/{model}.json", "w"), indent=1)
    print(model, "written")


if __name__ == "__main__":
    for m in sys.argv[1:] or ["clip", "siglip", "dinov2"]:
        main(m)
