#!/usr/bin/env python3
"""E10b — redo every Claude reading blind (E5 synthetic, E4b screens, E6 real), then judge.

Synthetic set: the 30 works of E5 x {orig, frame 1, wall 2, book 2, web 2, deep 3, deep 4,
deep 6} + the three controls (match, degr, clut) of book 2 and deep 6 = 14 images per work.
Screen set: the same 30 works x {CMY, colour only, blur only, CMYK medium, CMYK coarse},
subject call only. Real set: the 171 reproductions. Stages are rebuilt exactly as in E4 (v2).
"""

from __future__ import annotations

import importlib.util
import json
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

from punctured_sky.blind import judge, read
from punctured_sky.chains import CHAINS
from punctured_sky.claude_vision import Cache
from punctured_sky.corpus import load_works
from punctured_sky.layers import apply_chain

spec = importlib.util.spec_from_file_location("st", "scripts/e4_embed_stages.py")
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

SYN = [("orig", 0), ("frame", 1), ("wall", 2), ("book", 2), ("web", 2), ("deep", 3),
       ("deep", 4), ("deep", 6), ("match|book", 2), ("degr|book", 2), ("clut|book", 2),
       ("match|deep", 6), ("degr|deep", 6), ("clut|deep", 6)]
SCREENS = ["ht_cmy", "ht_cmy_colour", "ht_blur_only", "ht_cmyk_medium", "ht_cmyk_coarse"]
SRC = Path("data/blind/src")
READS = Cache("data/annotations/blind_readings.jsonl")
JUDGED = Cache("data/annotations/blind_judged.jsonl")


def e5_works():
    old = [json.loads(l) for l in open("data/annotations/e5_readings.jsonl")]
    ids = list(dict.fromkeys(r["work"] for r in old))
    by = {w["id"]: w for w in load_works()}
    return [by[i] for i in ids]


def build_synthetic(w) -> list[tuple[str, Path]]:
    paths = {(n, k): SRC / f"{w['id'].split(':')[1]}__{n.replace('|', '-')}__{k}.jpg"
             for n, k in SYN}
    if all(p.exists() for p in paths.values()):  # do not rebuild 67 stages for nothing
        return [(f"syn|{w['id']}|{n}|{k}", p) for (n, k), p in paths.items()]
    out, want = [], set(SYN)
    for name, k, area, im in st.stages_of(w):
        if (name, k) in want:
            p = SRC / f"{w['id'].split(':')[1]}__{name.replace('|', '-')}__{k}.jpg"
            if not p.exists():
                im.save(p, quality=92)
            out.append((f"syn|{w['id']}|{name}|{k}", p))
    return out


def build_screens(w) -> list[tuple[str, Path]]:
    im = Image.open(w["image_abspath"]).convert("RGB")
    out = []
    for v in SCREENS:
        p = SRC / f"{w['id'].split(':')[1]}__{v}.jpg"
        if not p.exists():
            apply_chain(im, CHAINS[v], zlib.crc32(f"{w['id']}|{v}".encode()))[1].save(p, quality=92)
        out.append((f"scr|{w['id']}|{v}|1", p))
    return out


def main(threads: int = 4) -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    works = e5_works()
    jobs = []
    for w in works:
        syn = build_synthetic(w)
        jobs += [(k, p, "subject") for k, p in syn] + [(k, p, "supports") for k, p in syn]
        jobs += [(k, p, "subject") for k, p in build_screens(w)]
    real = [json.loads(l) for l in open("data/real/manifest.jsonl")]
    for r in real:
        k, p = f"real|{r['work']}|{r['file']}|0", Path("data/real/images") / r["file"]
        jobs += [(k, p, "subject"), (k, p, "supports")]
    # most important first (subject everywhere, then layers on the real set, then layers on the
    # synthetic set, then the screens), so that a usage limit cuts the least useful part
    def priority(j):
        k, _, which = j
        return (k.startswith("scr|"), which != "subject", not k.startswith("real|"))
    jobs.sort(key=priority)
    todo = [j for j in jobs if f"{j[0]}#{j[2]}" not in READS]
    print(len(jobs), "readings,", len(todo), "to do", flush=True)
    with ThreadPoolExecutor(threads) as ex:
        for i, _ in enumerate(ex.map(lambda j: read(j[0], j[1], READS, j[2]), todo)):
            if i % 25 == 0:
                print(i, flush=True)
    # judge: per synthetic work (reference = blind reading of orig), per real work (reference =
    # the clean image's reading), per screen work (reference = orig)
    subj = {r["item"]: r for r in READS.data.values() if r.get("which") == "subject"
            and "error" not in r}
    for w in works:
        ref = subj[f"syn|{w['id']}|orig|0"]["subject"]
        items = {k: v["subject"] for k, v in subj.items()
                 if (k.startswith(f"syn|{w['id']}|") and not k.endswith("|orig|0"))
                 or k.startswith(f"scr|{w['id']}|")}
        judge(f"syn|{w['id']}", ref, items, JUDGED)
    for work in dict.fromkeys(r["work"] for r in real):
        mine = [r for r in real if r["work"] == work]
        ref_file = next(r["file"] for r in mine if r["support"] == "clean")
        ref = subj[f"real|{work}|{ref_file}|0"]["subject"]
        items = {f"real|{work}|{r['file']}|0": subj[f"real|{work}|{r['file']}|0"]["subject"]
                 for r in mine if r["file"] != ref_file and f"real|{work}|{r['file']}|0" in subj}
        judge(f"real|{work}", ref, items, JUDGED)
    print("done", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
