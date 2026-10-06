#!/usr/bin/env python3
"""Review 2 — round-2 analysis: share of descriptions where the work's subject is the main
subject / is named, per condition (subject asked alone), with intervals grouped by work, and
the paired contrasts that isolate each candidate cause:
  book vs book_notext  -> the readable text;   degr vs degclut -> being surrounded at all;
  degclut vs book_notext -> being *contained* by a support (same pixels, same place)."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

rng = np.random.default_rng(0)


def main() -> None:
    v = {}
    for l in open("data/annotations/blind2_judged.jsonl"):
        v.update(json.loads(l)["verdicts"])
    by = defaultdict(dict)  # cond -> work -> (named, main)
    for item, x in v.items():
        _, work, cond, _ = item.split("|")
        by[cond][work] = (float(bool(x.get("named"))), float(x.get("role") == "main"))
    works = sorted({w for d in by.values() for w in d})
    out = {"conditions": {}, "contrasts": {}}
    for cond, d in sorted(by.items()):
        main = np.array([d[w][1] for w in works if w in d])
        named = np.array([d[w][0] for w in works if w in d])
        bm = [rng.choice(main, len(main)).mean() for _ in range(2000)]
        out["conditions"][cond] = {"n": len(main), "main": float(main.mean()),
                                   "main_ci": np.percentile(bm, [2.5, 97.5]).tolist(),
                                   "named": float(named.mean())}
    for a, b, what in [("book", "book_notext", "texte lisible"),
                       ("degclut", "degr", "être entourée (mêmes pixels, même place)"),
                       ("book_notext", "degclut", "être contenue par un support (même place, mêmes pixels, sans texte)"),
                       ("book", "degr", "tout ce que le livre ajoute")]:
        diff = np.array([by[a][w][1] - by[b][w][1] for w in works if w in by[a] and w in by[b]])
        bd = [rng.choice(diff, len(diff)).mean() for _ in range(2000)]
        out["contrasts"][f"{a} - {b}"] = {"what": what, "diff_main": float(diff.mean()),
                                         "ci": np.percentile(bd, [2.5, 97.5]).tolist(),
                                         "n": len(diff)}
    Path("results/E10c").mkdir(parents=True, exist_ok=True)
    json.dump(out, open("results/E10c/round2.json", "w"), indent=1, ensure_ascii=False)
    for c, s in out["conditions"].items():
        print(f"{c:12s} n={s['n']:2d} principal {s['main']:.2f} [{s['main_ci'][0]:.2f},{s['main_ci'][1]:.2f}] nommé {s['named']:.2f}")
    for k, s in out["contrasts"].items():
        print(f"{k:24s} Δ principal {s['diff_main']:+.2f} [{s['ci'][0]:+.2f},{s['ci'][1]:+.2f}]  ({s['what']})")


if __name__ == "__main__":
    main()
