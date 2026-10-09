#!/usr/bin/env python3
"""Social round (pilot) — blind readings of the 100 images by Claude Sonnet: the subject asked
alone, then indirect questions that never mention a frame (title, place, period, price, owner,
is it art, three adjectives), in two separate calls; then a blind judgment of each subject
answer by Claude Haiku. Also prepares the same images, under the same opaque names, for the
Gemini agent (data/social/gemini/)."""

from __future__ import annotations

import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from punctured_sky.blind import SOCIAL, SUBJECT_ONLY, _call, opaque, read
from punctured_sky.claude_vision import Cache

ITEMS = json.loads(Path("data/social/items.json").read_text())
READS = Cache("data/annotations/social_readings.jsonl")
JUDGED = Cache("data/annotations/social_judged.jsonl")
GEM = Path("data/social/gemini")

WHAT = {
    "renoir": "une peinture : deux fillettes au piano, l'une debout avec une mandoline ou une partition",
    "mondrian": "une peinture abstraite : grands rectangles de couleur (rouge, bleu, gris) séparés de lignes noires",
    "child": "un dessin d'enfant : une maison jaune, un soleil, un nuage qui pleut",
    "beach": "une photographie : une plage de sable sous un ciel nuageux, avec une piscine ronde en béton",
    "receipt": "un ticket de caisse de supermarché",
}

JUDGE = """Une image montre, quelque part, l'objet suivant : {what}.
Voici une description de l'image écrite par quelqu'un d'autre :
« {desc} »
Réponds uniquement par un objet JSON :
{{"named": true si la description mentionne cet objet (même sans le reconnaître exactement), sinon false,
 "role": "main" si la description parle d'abord de cet objet, "complement" s'il n'y figure que comme élément d'autre chose (un mur, une pièce, un cadre…), "absent" s'il n'est pas mentionné,
 "as_artwork": true si la description présente cet objet comme une œuvre d'art (tableau, œuvre, toile encadrée, pièce de collection…), sinon false,
 "frame_mentioned": true si la description mentionne un cadre, sinon false,
 "room": "le type de lieu que la description attribue à l'image, en deux ou trois mots, ou \\"aucun\\""}}"""


def key(it: dict) -> str:
    return f"soc|{it['content']}|{it['frame']}|{it['space']}"


def main(threads: int = 2) -> None:
    items = ITEMS["items"]
    src = {key(it): Path("data/social/img") / it["file"] for it in items}
    # same opaque copies for Gemini
    (GEM / "img").mkdir(parents=True, exist_ok=True)
    for k, p in src.items():
        o = opaque(k, p)
        if not (GEM / "img" / o.name).exists():
            shutil.copy(o, GEM / "img" / o.name)
    (GEM / "PROMPTS.md").write_text(
        "# Deux questions par image, dans deux échanges séparés\n\n## subject_only\n\n"
        + SUBJECT_ONLY + "\n\n## social\n\n" + SOCIAL + "\n")
    if "--prepare-only" in sys.argv:
        print(len(src), "images prepared for Gemini in", GEM / "img")
        return
    jobs = [(k, p, w) for k, p in src.items() for w in ("subject_only", "social")
            if f"{k}#{w}" not in READS]
    print(len(jobs), "readings to do", flush=True)
    with ThreadPoolExecutor(threads) as ex:
        list(ex.map(lambda j: read(j[0], j[1], READS, j[2]), jobs))
    subj = {r["item"]: r["subject"] for r in READS.data.values() if "subject" in r}

    def one(k: str) -> None:
        if k in JUDGED or k not in subj:
            return
        prompt = JUDGE.format(what=WHAT[k.split("|")[1]], desc=subj[k])
        for _ in range(3):
            try:
                ans, mid = _call(prompt, "haiku")
                JUDGED.add(k, {"model": mid, **ans})
                return
            except Exception as e:  # noqa: BLE001
                last = str(e)
                if "limit" in last.lower():
                    raise
    with ThreadPoolExecutor(threads) as ex:
        list(ex.map(one, list(src)))
    print("done", flush=True)


if __name__ == "__main__":
    main()
