#!/usr/bin/env python3
"""E10b — second blind judgment: does the answer to 'which artwork is reproduced, and what
does it represent?' match the work's reference description? (recognised vs merely mentioned)"""

from __future__ import annotations

import json

from impressions.blind import judge
from impressions.claude_vision import Cache

READS = Cache("data/annotations/blind_readings.jsonl")
OUT = Cache("data/annotations/blind_judged_artwork.jsonl")


def main() -> None:
    subj = {r["item"]: r for r in READS.data.values() if r.get("which") == "subject"
            and "error" not in r}
    groups = {}
    for item, r in subj.items():
        kind, work = item.split("|")[0], item.split("|")[1]
        if kind == "scr":
            continue
        groups.setdefault(f"{kind}|{work}", {})[item] = r
    real = {json.loads(l)["file"]: json.loads(l) for l in open("data/real/manifest.jsonl")}
    for g, items in groups.items():
        if g.startswith("syn|"):
            ref_key = f"{g}|orig|0"
        else:
            ref_key = next(k for k in items if real[k.split("|")[2]]["support"] == "clean")
        ref = items[ref_key]["subject"]
        texts = {k: str(v.get("artwork", "")) for k, v in items.items() if k != ref_key}
        judge(f"art|{g}", ref, texts, OUT)
        print("judged", g, flush=True)


if __name__ == "__main__":
    main()
