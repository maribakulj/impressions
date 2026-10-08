#!/usr/bin/env python3
"""Round-2 analysis (subject asked alone). For each condition: how many descriptions make the
work's subject the main subject, a complement, or leave it out (Codex review: omission is not
subordination), with Wilson intervals; paired contrasts between conditions on the same works,
with discordant pairs and an exact McNemar test (bootstrap intervals collapse at 0/30 and 30/30).

Primary judgments: data/annotations/blind2b_judged.jsonl — the whole group re-judged after the
'book without text' condition was rebuilt with the book's exact geometry (book_notext2). The
first judgments (blind2_judged.jsonl, with the flawed book_notext) are kept and compared, which
also measures how stable the judge is on the seven conditions both runs share.
"""

from __future__ import annotations

import json
from collections import defaultdict
from math import comb, sqrt
from pathlib import Path

CONTRASTS = [
    ("book", "book_notext2", "texte lisible (même géométrie)"),
    ("degclut", "degr", "être entourée (mêmes pixels, même place)"),
    ("book_notext2", "degclut", "être contenue par un support plutôt qu'entourée d'un tableau "
                                "(mêmes pixels, même place, sans texte)"),
    ("book", "degr", "tout ce que le livre ajoute"),
    ("match", "degr", "dégradation et position (sur gris)"),
]


def load(path: str) -> dict[str, dict[str, str]]:
    """cond -> work -> 'main' | 'complement' | 'absent'."""
    by: dict[str, dict[str, str]] = defaultdict(dict)
    for line in open(path):
        for item, x in json.loads(line)["verdicts"].items():
            _, work, cond, _ = item.split("|")
            role = x.get("role") if x.get("named") else "absent"
            by[cond][work] = role if role in ("main", "complement") else "absent"
    return by


def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [max(0.0, c - h), min(1.0, c + h)]


def mcnemar(b: int, c: int) -> float:
    """Exact two-sided McNemar on discordant pairs b (a only) and c (b only)."""
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def summarise(by: dict[str, dict[str, str]]) -> dict:
    out = {"conditions": {}, "contrasts": {}}
    for cond, d in sorted(by.items()):
        n = len(d)
        counts = {r: sum(v == r for v in d.values()) for r in ("main", "complement", "absent")}
        out["conditions"][cond] = {"n": n, **counts, "main_share": counts["main"] / n,
                                   "main_wilson": wilson(counts["main"], n)}
    for a, b, what in CONTRASTS:
        if a not in by or b not in by:
            continue
        works = sorted(set(by[a]) & set(by[b]))
        only_a = sum(by[a][w] == "main" and by[b][w] != "main" for w in works)
        only_b = sum(by[b][w] == "main" and by[a][w] != "main" for w in works)
        out["contrasts"][f"{a} - {b}"] = {
            "what": what, "n": len(works), "diff_main": (only_a - only_b) / len(works),
            "main_only_first": only_a, "main_only_second": only_b,
            "mcnemar_exact_p": mcnemar(only_a, only_b)}
    return out


def main() -> None:
    new, old = load("data/annotations/blind2b_judged.jsonl"), load("data/annotations/blind2_judged.jsonl")
    out = summarise(new)
    shared = sorted(set(new) & set(old))
    agree = [new[c][w] == old[c][w] for c in shared for w in new[c] if w in old[c]]
    out["judge_stability"] = {"conditions": shared, "pairs": len(agree),
                              "same_verdict": sum(agree) / len(agree)}
    out["first_run_flawed_notext"] = summarise(old)["conditions"].get("book_notext")
    Path("results/E10c").mkdir(parents=True, exist_ok=True)
    json.dump(out, open("results/E10c/round2.json", "w"), indent=1, ensure_ascii=False)
    for c, s in out["conditions"].items():
        lo, hi = s["main_wilson"]
        print(f"{c:13s} n={s['n']:2d} principal {s['main']:2d} complément {s['complement']:2d} "
              f"absent {s['absent']:2d}   part principal {s['main_share']:.2f} [{lo:.2f}, {hi:.2f}]")
    for k, s in out["contrasts"].items():
        print(f"{k:24s} Δ {s['diff_main']:+.2f}  discordances {s['main_only_first']}/{s['main_only_second']}"
              f"  p={s['mcnemar_exact_p']:.2g}  ({s['what']})")
    j = out["judge_stability"]
    print(f"stabilité du juge : {j['same_verdict']:.1%} de verdicts identiques sur {j['pairs']} paires")


if __name__ == "__main__":
    main()
