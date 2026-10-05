#!/usr/bin/env python3
"""E6 — Claude reads the real reproductions with the E5 prompt; then, per work, the judge
compares each image's subject with the subject named on the work's clean reference(s)."""

from __future__ import annotations

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import importlib.util

from impressions.claude_vision import Cache, ask_json

spec = importlib.util.spec_from_file_location("e5", "scripts/e5_readings.py")
e5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e5)


def main() -> None:
    rows = [json.loads(l) for l in open("data/real/manifest.jsonl")]
    cache = Cache("data/annotations/e6_readings.jsonl")
    todo = [r for r in rows if r["file"] not in cache]

    def read(r):
        p = Path("data/real/images") / r["file"]
        for _ in range(3):
            try:
                return r, ask_json(str(p.resolve()), e5.READ)
            except Exception as e:  # noqa: BLE001
                err = str(e)
        return r, {"error": err[:200]}

    with ThreadPoolExecutor(3) as ex:
        for r, ans in ex.map(read, todo):
            cache.add(r["file"], {"work": r["work"], **ans})
            print(r["file"], flush=True)
    judged = Cache("data/annotations/e6_judged.jsonl")
    for work in dict.fromkeys(r["work"] for r in rows):
        if work in judged:
            continue
        mine = [r for r in rows if r["work"] == work]
        ref = next(r for r in mine if r["support"] == "clean")
        others = [r for r in mine if r["file"] != ref["file"]]
        versions = "\n".join(f'{r["file"]} — {cache.data[r["file"]].get("subject", "")}'
                             for r in others)
        prompt = e5.JUDGE.replace("{orig}", cache.data[ref["file"]].get("subject", "")).replace(
            "{versions}", versions)
        proc = subprocess.run(["claude", "-p", prompt, "--model", "sonnet", "--output-format",
                               "json"], capture_output=True, text=True, timeout=240)
        text = json.loads(proc.stdout)["result"]
        judged.add(work, {"reference": ref["file"],
                          "verdicts": json.loads(text[text.index("{"):text.rindex("}") + 1])})
        print("judged", work, flush=True)


if __name__ == "__main__":
    main()
