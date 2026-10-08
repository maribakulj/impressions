#!/usr/bin/env python3
"""E7 — the human study package, rebuilt after Codex's review (08/10/2026): the first version
tested an abandoned hypothesis (depth six, where the work is too small to see).

It now asks people what Claude was asked in round 2, on the very same images: 12 of the 30
round-2 works x 6 conditions = 72 images, in 6 lists by a Latin square, so that each person
sees each work once (otherwise they would recognise it under the layers) and each condition
twice. The subject question is shown alone first, as in round 2; the other questions come after.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import random
import shutil
from pathlib import Path

spec = importlib.util.spec_from_file_location("r2", "scripts/blind_round2.py")
r2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r2)

CONDITIONS = ["degr", "degclut", "book", "book_notext2", "web", "wall"]
N_WORKS = 12
OUT = Path("human_study")


def main() -> None:
    works = r2.br.e5_works()
    rng = random.Random(2026_10_08)
    chosen = rng.sample(works, N_WORKS)
    img_dir = OUT / "images"
    shutil.rmtree(img_dir, ignore_errors=True)
    img_dir.mkdir(parents=True)
    rows = []
    n = len(CONDITIONS)
    for i, w in enumerate(chosen):
        key = w["id"].split(":")[1]
        for j, cond in enumerate(CONDITIONS):
            img_id = f"i{rng.randrange(16 ** 6):06x}"
            shutil.copy(r2.SRC / f"{key}__{cond}.jpg", img_dir / f"{img_id}.jpg")
            rows.append({"image": f"images/{img_id}.jpg", "list": (i + j) % n + 1,
                         "work": w["id"], "kind": w["kind"], "condition": cond})
    with open(OUT / "items.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    lists = {str(k): [r["image"] for r in rows if r["list"] == k] for k in range(1, n + 1)}
    for k in lists:
        rng.shuffle(lists[k])
    (OUT / "lists.json").write_text(json.dumps(lists, indent=1))
    form = (OUT / "form_template.html").read_text()
    (OUT / "form.html").write_text(form.replace("__LISTS__", json.dumps(lists, indent=1))
                                   .replace("__NLISTS__", "".join(f"<option>{k}</option>" for k in lists)))
    per_list = {k: sorted(r["condition"] for r in rows if r["list"] == int(k)) for k in lists}
    assert all(len(v) == N_WORKS and all(v.count(c) == N_WORKS // n for c in CONDITIONS)
               for v in per_list.values())
    print({k: len(v) for k, v in lists.items()}, "images per list; each condition",
          N_WORKS // n, "times; each work once")


if __name__ == "__main__":
    main()
