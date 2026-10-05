#!/usr/bin/env python3
"""E1 — a stratified sample of works: 60 per object type, one per near-duplicate group,
spread over Iconclass divisions, images at least 600 px on the short side."""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

from PIL import Image

from impressions.corpus import load_pool
from impressions.sheets import contact_sheet

PER_TYPE = 60
KINDS = ["painting", "print", "drawing", "sculpture", "photograph"]


def main() -> None:
    rng = random.Random(20261005)
    pool = load_pool()
    chosen = []
    for kind in KINDS:
        rows = [r for r in pool if r["kind"] == kind]
        rng.shuffle(rows)
        by_division = defaultdict(list)
        for r in rows:
            by_division[r["iconclass"][0][:1]].append(r)
        seen_groups, picked = set(), []
        # round-robin over Iconclass divisions so no single subject dominates
        while len(picked) < PER_TYPE and any(by_division.values()):
            for div in sorted(by_division):
                if not by_division[div] or len(picked) >= PER_TYPE:
                    continue
                r = by_division[div].pop()
                if r["near_duplicate_group"] in seen_groups:
                    continue
                with Image.open(r["image_abspath"]) as im:
                    if min(im.size) < 600:
                        continue
                seen_groups.add(r["near_duplicate_group"])
                picked.append(r)
        chosen += picked
        print(kind, len(picked))
    out = Path("data/works.jsonl")
    with out.open("w") as fh:
        for r in chosen:
            fh.write(json.dumps({k: r[k] for k in (
                "id", "kind", "collection", "iconclass", "depicts", "inception",
                "image_path", "image_url", "source_url")}) + "\n")
    sample = rng.sample(chosen, 25)
    sheet = contact_sheet([(Image.open(r["image_abspath"]),
                            f"{r['kind']} {r['iconclass'][0]}\n{r['id']}") for r in sample])
    Path("figures").mkdir(exist_ok=True)
    sheet.save("figures/E1-works.jpg", quality=85)
    print("wrote", out, len(chosen))


if __name__ == "__main__":
    main()
