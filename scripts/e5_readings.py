#!/usr/bin/env python3
"""E5 — what Claude says each stage *is* (H3: does it count the layers? H4: does the subject
it names survive the layers?).

30 works (6 per object type) x 9 stages; the stages are rebuilt with the same seeds as E4.
Each image is read once with a fixed prompt; then, per work, one text-only call judges whether
the subject named at each stage is the subject named for the original.
"""

from __future__ import annotations

import json
import random
import subprocess
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

from impressions.chains import CHAINS
from impressions.claude_vision import Cache, ask_json
from impressions.corpus import load_works
from impressions.layers import apply_chain, area_matched, content_mask

STAGES = [("orig", 0), ("frame", 1), ("wall", 2), ("book", 2), ("web", 2), ("print", 2),
          ("deep", 4), ("deep", 6), ("match|deep", 6)]
OUT = Path("data/layers/e5")

READ = """Réponds uniquement par un objet JSON avec ces clés :
- "subject": en une phrase, ce que l'image représente (ce qu'on y voit figuré) ;
- "chain": la liste ordonnée des supports et cadres que tu vois, de l'extérieur vers
  l'intérieur, jusqu'à l'œuvre (ex. ["photo d'écran", "page web", "photo de livre", "page
  imprimée", "photo de musée", "cadre doré", "peinture"]) ;
- "n_layers": le nombre de couches entre le bord de l'image et l'œuvre elle-même (0 si l'œuvre
  occupe toute l'image) ;
- "work_kind": le type de l'œuvre la plus intérieure (peinture, estampe, dessin, sculpture,
  photographie, objet, autre) ;
- "synthetic": true si tu penses que des couches ont été ajoutées numériquement (montage),
  false sinon."""

JUDGE = """Voici la description du sujet d'une image originale, puis celles de versions de la
même image vue à travers différents supports. Pour chaque version, dis si la description
désigne le même sujet figuré que l'original : "same" (même sujet, même scène ou même figure),
"partial" (un trait commun mais la scène n'est pas reconnue), "support" (la description parle du
support — livre, écran, mur, cadre — au lieu du sujet figuré), ou "other" (un autre sujet).
Réponds uniquement par un objet JSON {"<id de version>": "same"|"partial"|"support"|"other"}.

ORIGINAL : {orig}

VERSIONS :
{versions}"""


def build(w) -> list[tuple[str, int, Path]]:
    im = Image.open(w["image_abspath"]).convert("RGB")
    key = w["id"].split(":")[1]
    out = []
    for name, k in STAGES:
        p = OUT / f"{key}_{name.replace('|', '-')}_{k}.jpg"
        if not p.exists():
            if name == "orig":
                st = apply_chain(im, [], 0)[0]
            elif name.startswith("match|"):
                base = name.split("|")[1]
                seed = zlib.crc32(f"{w['id']}|{base}".encode())
                stage = apply_chain(im, CHAINS[base], seed)[k]
                area = content_mask(im.size, CHAINS[base], seed)[k].mean()
                st = area_matched(im, stage.size, float(area))
            else:
                seed = zlib.crc32(f"{w['id']}|{name}".encode())
                st = apply_chain(im, CHAINS[name], seed)[k]
            st.save(p, quality=90)
        out.append((name, k, p))
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(55)
    works = load_works()
    pick = []
    for kind in ["painting", "print", "drawing", "sculpture", "photograph"]:
        pick += rng.sample([w for w in works if w["kind"] == kind], 6)
    jobs = [(w, name, k, p) for w in pick for name, k, p in build(w)]
    cache = Cache("data/annotations/e5_readings.jsonl")
    todo = [j for j in jobs if str(j[3]) not in cache]
    print(len(jobs), "stages,", len(todo), "to read", flush=True)

    def read(job):
        w, name, k, p = job
        for attempt in range(3):
            try:
                return job, ask_json(str(p.resolve()), READ)
            except Exception as e:  # noqa: BLE001
                err = str(e)
        return job, {"error": err[:200]}

    with ThreadPoolExecutor(3) as ex:
        for i, ((w, name, k, p), ans) in enumerate(ex.map(read, todo)):
            cache.add(str(p), {"work": w["id"], "kind": w["kind"], "chain_name": name, "k": k,
                               **ans})
            print(i, w["id"], name, k, "error" in ans, flush=True)
    judged = Cache("data/annotations/e5_judged.jsonl")
    for w in pick:
        if w["id"] in judged:
            continue
        rows = [cache.data[str(p)] for name, k, p in build(w)]
        orig = rows[0].get("subject", "")
        versions = "\n".join(f'{r["chain_name"]}:{r["k"]} — {r.get("subject", "")}'
                             for r in rows[1:])
        prompt = JUDGE.replace("{orig}", orig).replace("{versions}", versions)
        proc = subprocess.run(["claude", "-p", prompt, "--model", "sonnet", "--output-format",
                               "json"], capture_output=True, text=True, timeout=240)
        text = json.loads(proc.stdout)["result"]
        verdict = json.loads(text[text.index("{"):text.rindex("}") + 1])
        judged.add(w["id"], {"verdicts": verdict})
        print("judged", w["id"], flush=True)


if __name__ == "__main__":
    main()
