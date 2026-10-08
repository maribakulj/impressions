#!/usr/bin/env python3
"""Codex review (06/10): the round-2 'book without text' did not keep the geometry of the book
(skipped random draws changed the perspective). Fixed in layers.py; this rebuilds that one
condition under a new key ('book_notext2'), checks that the work's mask is now identical to the
book's, reads it blind (subject asked alone) and re-judges each work's whole group in a separate
cache, so that the first judgments stay untouched and the judge's stability can be compared.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

from punctured_sky.blind import judge, read
from punctured_sky.chains import CHAINS
from punctured_sky.claude_vision import Cache
from punctured_sky.layers import apply_chain, content_mask

spec = importlib.util.spec_from_file_location("r2", "scripts/blind_round2.py")
r2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r2)

JUDGED = Cache("data/annotations/blind2b_judged.jsonl")
NAME = "book_notext2"


def build(w) -> tuple[str, Path, float]:
    key = w["id"].split(":")[1]
    path = r2.SRC / f"{key}__{NAME}.jpg"
    im = Image.open(w["image_abspath"]).convert("RGB")
    seed = zlib.crc32(f"{w['id']}|book".encode())
    m_book = content_mask(im.size, CHAINS["book"], seed)[2]
    m_note = content_mask(im.size, CHAINS["book_notext"], seed)[2]
    iou = float((m_book & m_note).sum() / (m_book | m_note).sum())
    if not path.exists():
        apply_chain(im, CHAINS["book_notext"], seed)[2].save(path, quality=92)
    return f"r2|{w['id']}|{NAME}|0", path, iou


def main(threads: int = 2) -> None:
    works = r2.br.e5_works()
    jobs = [build(w) for w in works]
    ious = [j[2] for j in jobs]
    print(f"mask IoU book vs book_notext2: min {min(ious):.4f}, mean {np.mean(ious):.4f}")
    assert min(ious) > 0.999, "geometry still differs"
    if "--build-only" in sys.argv:
        return
    todo = [j for j in jobs if f"{j[0]}#subject_only" not in r2.READS]
    print(len(todo), "readings to do", flush=True)
    with ThreadPoolExecutor(threads) as ex:
        list(ex.map(lambda j: read(j[0], j[1], r2.READS, "subject_only"), todo))
    subj = {r["item"]: r["subject"] for r in r2.READS.data.values() if "subject" in r}
    for w in works:
        ref = subj[f"r2|{w['id']}|orig|0"]
        items = {k: v for k, v in subj.items() if k.startswith(f"r2|{w['id']}|")
                 and not k.endswith("|orig|0") and "|book_notext|" not in k}
        judge(f"r2b|{w['id']}", ref, items, JUDGED)
    print("done", json.dumps({"n": len(works)}), flush=True)


if __name__ == "__main__":
    main()
