#!/usr/bin/env python3
"""E7 — the human study package (prepared, not run).

8 works from the E5 subsample (so Claude's readings of the very same images exist) x 5 stages
(original, gilt frame, photographed book, depth 4, depth 6) = 40 images, arranged in 5 lists by
a Latin square: each participant sees each work once and each stage 1-2 times, 8 images in all.
The questions are the ones Claude answered in E5, in plain words.
"""

from __future__ import annotations

import csv
import json
import random
import shutil
from pathlib import Path

STAGES = [("orig", 0), ("frame", 1), ("book", 2), ("deep", 4), ("deep", 6)]
KINDS = ["painting", "painting", "print", "print", "drawing", "sculpture", "sculpture",
         "photograph"]


def main() -> None:
    reads = [json.loads(l) for l in open("data/annotations/e5_readings.jsonl")]
    by_work = {}
    for r in reads:
        by_work.setdefault(r["work"], {})[(r["chain_name"], r["k"])] = r
    rng = random.Random(77)
    chosen = []
    for kind in KINDS:
        pool = [w for w, d in by_work.items() if d[("orig", 0)]["kind"] == kind
                and w not in chosen]
        chosen.append(rng.choice(pool))
    out = Path("human_study")
    rows = []
    for i, w in enumerate(chosen):
        for j, (name, k) in enumerate(STAGES):
            src = Path(by_work[w][(name, k)]["key"])
            img_id = f"img{i}{j}"
            shutil.copy(src, out / "images" / f"{img_id}.jpg")
            lst = (i + j) % 5 + 1  # Latin square over works x stages
            rows.append({"image": f"images/{img_id}.jpg", "list": lst, "work": w,
                         "kind": by_work[w][(name, k)]["kind"], "stage": f"{name}|{k}"})
    with open(out / "items.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    lists = {n: [r["image"] for r in rows if r["list"] == n] for n in range(1, 6)}
    for n in lists:
        rng.shuffle(lists[n])
    (out / "lists.json").write_text(json.dumps(lists, indent=1))
    print({n: len(v) for n, v in lists.items()})


if __name__ == "__main__":
    main()
