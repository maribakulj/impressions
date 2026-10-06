#!/usr/bin/env python3
"""Review 2 — is it being *contained* that demotes the work, or the readable text, the
photographic scene, the off-centre position? Same 30 works; subject asked alone, in its own call.

Conditions (book chain, two layers, same seed as E4 so that the geometry is identical):
book (as in E4), book without any text, the same degraded pixels at the same place on grey
('degr'), the same degraded pixels at the same place on a busy painting ('degclut'), the work
alone centred at the same area ('match'), the work centred on a busy painting ('clut'), plus the
original, the wall and the web page for reference.
"""

from __future__ import annotations

import importlib.util
import random
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

from punctured_sky.blind import judge, read
from punctured_sky.chains import CHAINS
from punctured_sky.claude_vision import Cache
from punctured_sky.layers import (apply_chain, area_matched, clutter_matched, content_mask,
                                  degraded_matched, degraded_on_clutter)

spec = importlib.util.spec_from_file_location("br", "scripts/blind_readings.py")
br = importlib.util.module_from_spec(spec)
spec.loader.exec_module(br)

SRC = Path("data/blind/src2")
READS = Cache("data/annotations/blind2_readings.jsonl")
JUDGED = Cache("data/annotations/blind2_judged.jsonl")


def build(w) -> list[tuple[str, Path]]:
    key = w["id"].split(":")[1]
    names = ["orig", "book", "book_notext", "degr", "degclut", "match", "clut", "wall", "web"]
    paths = {n: SRC / f"{key}__{n}.jpg" for n in names}
    if not all(p.exists() for p in paths.values()):
        im = Image.open(w["image_abspath"]).convert("RGB")
        seed = zlib.crc32(f"{w['id']}|book".encode())
        book = apply_chain(im, CHAINS["book"], seed)[2]
        notext = apply_chain(im, CHAINS["book_notext"], seed)[2]
        mask = content_mask(im.size, CHAINS["book"], seed)[2]
        bg = Image.open(random.Random(seed + 2).choice(br.st.backgrounds()))
        imgs = {
            "orig": apply_chain(im, [], 0)[0], "book": book, "book_notext": notext,
            "degr": degraded_matched(book, mask), "degclut": degraded_on_clutter(book, mask, bg),
            "match": area_matched(im, book.size, float(mask.mean())),
            "clut": clutter_matched(im, book.size, float(mask.mean()), bg),
            "wall": apply_chain(im, CHAINS["wall"], zlib.crc32(f"{w['id']}|wall".encode()))[2],
            "web": apply_chain(im, CHAINS["web"], zlib.crc32(f"{w['id']}|web".encode()))[2],
        }
        for n, img in imgs.items():
            img.save(paths[n], quality=92)
    return [(f"r2|{w['id']}|{n}|0", p) for n, p in paths.items()]


def main(threads: int = 2) -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    works = br.e5_works()
    jobs = [j for w in works for j in build(w)]
    if "--build-only" in sys.argv:
        print(len(jobs), "images built")
        return
    todo = [j for j in jobs if f"{j[0]}#subject_only" not in READS]
    print(len(jobs), "readings,", len(todo), "to do", flush=True)
    with ThreadPoolExecutor(threads) as ex:
        list(ex.map(lambda j: read(j[0], j[1], READS, "subject_only"), todo))
    subj = {r["item"]: r["subject"] for r in READS.data.values() if "subject" in r}
    for w in works:
        ref = subj[f"r2|{w['id']}|orig|0"]
        items = {k: v for k, v in subj.items() if k.startswith(f"r2|{w['id']}|")
                 and not k.endswith("|orig|0")}
        judge(f"r2|{w['id']}", ref, items, JUDGED)
    print("done", flush=True)


if __name__ == "__main__":
    main()
