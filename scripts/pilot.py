#!/usr/bin/env python3
"""E3 — pilot to look at: 3 works x every chain; per stage, the 3 nearest pool images for
each model, the rank of the work's own museum image, and Claude's reading of the stage."""

from __future__ import annotations

import json
import zlib
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from impressions.chains import CHAINS
from impressions.claude_vision import Cache, ask
from impressions.corpus import load_works
from impressions.encoders import Encoder
from impressions.gallery import Gallery
from impressions.layers import apply_chain

PROMPT = ("En une phrase, que représente cette image ? Puis, en une phrase, qu'est-ce que tu "
          "regardes physiquement (quel objet, quel support) ? Réponds en deux lignes : "
          "« Sujet : … » et « Support : … ».")
OUT = Path("data/layers/pilot")
MODELS = ["clip", "siglip", "dinov2"]


def main() -> None:
    works = load_works()
    rng = random.Random(11)
    pick = [rng.choice([w for w in works if w["kind"] == k])
            for k in ("painting", "sculpture", "print")]
    OUT.mkdir(parents=True, exist_ok=True)
    stages = []  # (work, chain, k, path)
    for w in pick:
        im = Image.open(w["image_abspath"])
        for name, chain in CHAINS.items():
            for k, st in enumerate(apply_chain(im, chain, seed=zlib.crc32(w["id"].encode()))):
                if k == 0 and name != "frame":
                    continue
                p = OUT / f"{w['id'].split(':')[1]}_{name}_{k}.jpg"
                st.save(p, quality=90)
                stages.append((w, "orig" if k == 0 else name, k, p))
    results = {m: {} for m in MODELS}
    for m in MODELS:
        enc, gal = Encoder(m), Gallery(m)
        vecs = enc.images(Image.open(p) for *_, p in stages)
        for (w, name, k, p), v in zip(stages, vecs):
            results[m][str(p)] = {
                "rank_self": gal.rank_of(v, w["id"]),
                "nn": [(r["id"], r["kind"], r["iconclass"][0], round(s, 3))
                       for r, s in gal.neighbours(v, 3, exclude=w["id"])],
            }
    cache = Cache("data/annotations/pilot_readings.jsonl")
    for w, name, k, p in stages:
        if str(p) not in cache:
            cache.add(str(p), {"answer": ask(str(p.resolve()), PROMPT)})
    rows = []
    for w, name, k, p in stages:
        rows.append({"work": w["id"], "kind": w["kind"], "iconclass": w["iconclass"],
                     "chain": name, "k": k, "path": str(p),
                     **{m: results[m][str(p)] for m in MODELS},
                     "claude": cache.data[str(p)]["answer"]})
    Path("results/E3").mkdir(parents=True, exist_ok=True)
    with open("results/E3/pilot.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    render(rows)


def render(rows: list[dict]) -> None:
    """One sheet per work: a row per stage = stage, then 3 neighbours for CLIP and DINOv2."""
    from impressions.corpus import CAYPOLLARD, load_pool

    pool = {r["id"]: r for r in load_pool()}
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    cell = 150
    for wid in dict.fromkeys(r["work"] for r in rows):
        sub = [r for r in rows if r["work"] == wid]
        sheet = Image.new("RGB", (cell * 7 + 330, len(sub) * (cell + 6)), "white")
        d = ImageDraw.Draw(sheet)
        for i, r in enumerate(sub):
            y = i * (cell + 6)
            ims = [Image.open(r["path"])]
            for m in ("clip", "dinov2"):
                ims += [Image.open(CAYPOLLARD / pool[n[0]]["image_path"]) for n in r[m]["nn"]]
            for j, im in enumerate(ims):
                t = im.convert("RGB")
                t.thumbnail((cell - 6, cell - 6))
                sheet.paste(t, (j * cell + (j > 0) * 0 + (j > 3) * 10, y))
            txt = (f"{r['chain']} k={r['k']}\nrang soi CLIP {r['clip']['rank_self']} "
                   f"SigLIP {r['siglip']['rank_self']} DINO {r['dinov2']['rank_self']}\n"
                   f"CLIP nn: {', '.join(n[1] for n in r['clip']['nn'])}\n"
                   f"DINO nn: {', '.join(n[1] for n in r['dinov2']['nn'])}\n")
            claude = r["claude"].replace("\n", " ")
            lines = [claude[k:k + 52] for k in range(0, min(len(claude), 364), 52)]
            d.multiline_text((7 * cell + 14, y + 2), txt + "\n".join(lines), fill="black",
                             font=font, spacing=2)
        sheet.save(f"figures/E3-pilot-{wid.split(':')[1]}.jpg", quality=85)


if __name__ == "__main__":
    main()
