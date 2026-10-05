#!/usr/bin/env python3
"""E5 — H3/H4 for the caption-trained encoders (CLIP, SigLIP), zero-shot.

(a) Outermost support: which of 10 phrases best matches each stage? Scored against the layer
    actually added last ('none' for originals, area-matched controls and the shrink/JPEG
    controls). Baseline: always the most frequent class.
(b) Object type: which of 5 phrases ('a painting', 'a print', ...) best matches? Scored per
    stage against the work's museum type — does the support change the medium the model reads?
Reads the per-work caches written by e4_embed_stages.py, so it can run on a partial cache.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from impressions import CACHE
import numpy as np

from impressions.chains import CHAINS
from impressions.corpus import load_works
from impressions.encoders import Encoder

SUPPORTS = {
    "none": "a museum photograph of an artwork",
    "gilt_frame": "a picture in an ornate gilded frame",
    "mat_border": "a picture in a white mat board",
    "museum_wall": "a framed picture hanging on a gallery wall",
    "book_page": "a printed page of an art book with an illustration and a caption",
    "book_photo": "a photo of an open book lying on a table",
    "screenshot_ui": "a screenshot of a museum collection website",
    "screen_photo": "a photo of a computer monitor showing an image",
    "halftone_print": "a halftone printed reproduction with visible dots",
    "rephotograph": "a casual photo of a printed picture lying on a surface",
}
KINDS = {"painting": "a painting", "print": "a print, an engraving", "drawing": "a drawing",
         "sculpture": "a sculpture", "photograph": "an old photograph"}


def outermost(chain: str, k: int) -> str:
    if chain == "orig" or chain.startswith("match|") or chain.startswith("ctrl"):
        return "none"
    return CHAINS[chain][k - 1]


def main(model: str) -> dict:
    enc = Encoder(model)
    s_names = list(SUPPORTS)
    k_names = list(KINDS)
    t_sup = enc.texts([f"a photo of {SUPPORTS[s]}" if model == "clip" else SUPPORTS[s]
                       for s in s_names])
    t_kind = enc.texts([f"a photo of {KINDS[k]}" for k in k_names])
    works = {w["id"]: w for w in load_works()}
    stats = defaultdict(lambda: defaultdict(list))
    confusion = defaultdict(lambda: defaultdict(int))
    n = 0
    for meta_path in sorted((CACHE / "stages").glob("*.json")):
        vec_path = Path(f"{CACHE}/stages/{model}/{meta_path.stem}.npy")
        if not vec_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        vecs = np.load(vec_path).astype(np.float32)
        vecs /= np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-8
        n += 1
        for (wid, chain, k, area), v in zip(meta, vecs):
            truth = outermost(chain, k)
            guess = s_names[int(np.argmax(t_sup @ v))]
            kind_guess = k_names[int(np.argmax(t_kind @ v))]
            key = f"{chain}|{k}"
            stats[key]["support_ok"].append(guess == truth)
            stats[key]["kind_ok"].append(kind_guess == works[wid]["kind"])
            stats[key]["guess"].append(guess)
            stats[key]["kind_guess"].append(kind_guess)
            confusion[truth][guess] += 1
    all_truth = [t for t, row in confusion.items() for g, c in row.items() for _ in range(c)]
    majority = max(set(all_truth), key=all_truth.count)
    acc = np.mean([g == t for t, row in confusion.items() for g, c in row.items()
                   for _ in range(c)])
    recalls = [confusion[t][t] / sum(confusion[t].values()) for t in confusion]
    out = {
        "model": model, "works": n,
        "support_balanced_accuracy": float(np.mean(recalls)),
        "support_chance": 1 / len(s_names),
        "support_recall": {t: confusion[t][t] / sum(confusion[t].values()) for t in confusion},
        "support_accuracy": float(acc),
        "support_majority_baseline": float(all_truth.count(majority) / len(all_truth)),
        "stages": {k: {"support_ok": float(np.mean(v["support_ok"])),
                       "kind_ok": float(np.mean(v["kind_ok"])),
                       "top_guess": max(set(v["guess"]), key=v["guess"].count),
                       "kind_guesses": {g: v["kind_guess"].count(g) for g in set(v["kind_guess"])}}
                   for k, v in stats.items()},
        "confusion": {t: dict(r) for t, r in confusion.items()},
    }
    Path("results/E5").mkdir(parents=True, exist_ok=True)
    json.dump(out, open(f"results/E5/zeroshot-{model}.json", "w"), indent=1)
    return out


if __name__ == "__main__":
    for m in sys.argv[1:] or ["clip", "siglip"]:
        o = main(m)
        print(m, o["works"], "works; support balanced acc",
              round(o["support_balanced_accuracy"], 3), "chance 0.1;",
              {t: round(r, 2) for t, r in o["support_recall"].items()})
        for k, s in o["stages"].items():
            if not k.startswith("match"):
                print(f"  {k:16s} support {s['support_ok']:.2f}  type {s['kind_ok']:.2f}  "
                      f"→ {s['top_guess']:14s} types lus {s['kind_guesses']}")
