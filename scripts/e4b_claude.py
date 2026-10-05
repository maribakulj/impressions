#!/usr/bin/env python3
"""E4b — Claude on the screen variants: was the pilot's 'painting read as gilded relief' the
colour cast of the CMY screen, or the dots? Same 30 works and prompts as E5."""

from __future__ import annotations

import json
import subprocess
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

from impressions.chains import CHAINS
from impressions.claude_vision import Cache, ask_json
from impressions.corpus import load_works

import importlib.util

spec = importlib.util.spec_from_file_location("e5", "scripts/e5_readings.py")
e5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e5)

VARIANTS = ["ht_cmy", "ht_cmy_colour", "ht_cmyk_medium", "ht_cmyk_coarse"]
OUT = Path("data/layers/e4b")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    reads = [json.loads(l) for l in open("data/annotations/e5_readings.jsonl")]
    wids = list(dict.fromkeys(r["work"] for r in reads))
    works = {w["id"]: w for w in load_works()}
    jobs = []
    for wid in wids:
        w = works[wid]
        im = Image.open(w["image_abspath"]).convert("RGB")
        for v in VARIANTS:
            p = OUT / f"{wid.split(':')[1]}_{v}.jpg"
            if not p.exists():
                from impressions.layers import apply_chain
                apply_chain(im, CHAINS[v], zlib.crc32(f"{wid}|{v}".encode()))[1].save(p, quality=92)
            jobs.append((wid, v, p))
    cache = Cache("data/annotations/e4b_readings.jsonl")
    todo = [j for j in jobs if str(j[2]) not in cache]

    def read(job):
        for _ in range(3):
            try:
                return job, ask_json(str(job[2].resolve()), e5.READ)
            except Exception as e:  # noqa: BLE001
                err = str(e)
        return job, {"error": err[:200]}

    with ThreadPoolExecutor(3) as ex:
        for (wid, v, p), ans in ex.map(read, todo):
            cache.add(str(p), {"work": wid, "variant": v, "kind": works[wid]["kind"], **ans})
            print(wid, v, flush=True)
    judged = Cache("data/annotations/e4b_judged.jsonl")
    origs = {r["work"]: r for r in reads if r["chain_name"] == "orig"}
    for wid in wids:
        if wid in judged:
            continue
        rows = [cache.data[str(OUT / f"{wid.split(':')[1]}_{v}.jpg")] for v in VARIANTS]
        versions = "\n".join(f'{r["variant"]}:1 — {r.get("subject", "")}' for r in rows)
        prompt = e5.JUDGE.replace("{orig}", origs[wid]["subject"]).replace("{versions}", versions)
        proc = subprocess.run(["claude", "-p", prompt, "--model", "sonnet", "--output-format",
                               "json"], capture_output=True, text=True, timeout=240)
        text = json.loads(proc.stdout)["result"]
        judged.add(wid, {"verdicts": json.loads(text[text.index("{"):text.rindex("}") + 1])})


if __name__ == "__main__":
    main()
