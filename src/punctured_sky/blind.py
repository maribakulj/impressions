"""Blind readings (review B1, B2, I9).

Every image is copied under an opaque random name before Claude reads it; the table from
opaque name to condition is kept outside the folder Claude is pointed at. The subject is asked
in one call, the supports in another, neither with an example. The judge sees opaque ids in a
shuffled order, and is a different model (Opus) from the reader (Sonnet). The exact model id
is stored with every answer.
"""

from __future__ import annotations

import json
import random
import re
import secrets
import shutil
import subprocess
from pathlib import Path

from punctured_sky.claude_vision import Cache

BLIND_DIR = Path("data/blind/img")
MAP = Path("data/blind/map.jsonl")

SUBJECT = """Regarde cette image et réponds uniquement par un objet JSON :
{"subject": "en une phrase, ce que représente cette image",
 "artwork": "si une œuvre d'art est reproduite ou visible dans l'image : laquelle (titre et auteur si tu les reconnais, sinon une description courte) et ce qu'elle représente ; sinon \\"aucune\\"",
 "work_kind": "le type de cette œuvre : peinture, estampe, dessin, sculpture, photographie, objet, autre, ou aucune"}"""

SUBJECT_ONLY = """Regarde cette image et réponds uniquement par un objet JSON :
{"subject": "en une phrase, ce que représente cette image"}"""

SOCIAL = """Regarde cette image et réponds uniquement par un objet JSON :
{"titre": "un titre court pour cette image, comme dans une légende",
 "lieu": "où se trouve ce qu'on voit (le type de lieu)",
 "epoque": "de quelle époque date ce qu'on voit, au mieux",
 "prix_euros": "si l'objet principal de l'image était vendu, son prix probable en euros (un nombre)",
 "proprietaire": "à qui appartient probablement ce qu'on voit",
 "art": "oui, non ou incertain : cette image montre-t-elle une œuvre d'art ?",
 "adjectifs": "trois adjectifs qui décrivent l'image"}"""

SUPPORTS = """Regarde cette image et réponds uniquement par un objet JSON :
{"chain": "la liste ordonnée, de l'extérieur vers l'intérieur, des supports, cadres, écrans, pages, objets ou lieux qui s'interposent entre le bord de l'image et l'œuvre d'art la plus intérieure",
 "n_layers": "le nombre entier de ces couches (0 si l'œuvre occupe toute l'image)",
 "synthetic": "true si tu penses que certaines couches ont été ajoutées par montage numérique, sinon false"}"""

JUDGE = """Une même œuvre d'art a été décrite plusieurs fois, à partir d'images différentes.
Voici la description de RÉFÉRENCE de ce qu'elle représente, puis d'autres descriptions, chacune
précédée d'un identifiant. Pour chaque identifiant, dis :
- "named" : true si la description désigne reconnaissablement le même sujet figuré que la
  référence (même scène, même figure, même objet), où que ce soit dans la phrase ; sinon false ;
- "role" : "main" si ce sujet est ce dont la phrase parle principalement, "complement" s'il
  n'apparaît que comme élément d'autre chose (ce que montre un écran, un livre, une salle, ce
  devant quoi se tiennent des gens…), "absent" s'il n'est pas nommé.
Réponds uniquement par un objet JSON {"<id>": {"named": true|false, "role": "main"|"complement"|"absent"}}.

RÉFÉRENCE : {ref}

DESCRIPTIONS :
{items}"""


import threading

_LOCK = threading.Lock()


def opaque(key: str, src: Path) -> Path:
    """Copy src under an opaque name (once per key) and return the copy's path. Locked: two
    threads used to create two copies of the same key (review 2)."""
    with _LOCK:
        return _opaque(key, src)


def _opaque(key: str, src: Path) -> Path:
    BLIND_DIR.mkdir(parents=True, exist_ok=True)
    known = {}
    if MAP.exists():
        for line in MAP.open():
            row = json.loads(line)
            known[row["key"]] = row["file"]
    if key not in known:
        name = secrets.token_hex(6) + src.suffix.lower()
        shutil.copy(src, BLIND_DIR / name)
        with MAP.open("a") as fh:
            fh.write(json.dumps({"key": key, "file": name, "source": str(src)}) + "\n")
        known[key] = name
    return (BLIND_DIR / known[key]).resolve()


def _call(prompt: str, model: str, image: Path | None = None, timeout: int = 300) -> tuple[dict, str]:
    full = (f"Lis l'image {image} avec l'outil Read, puis réponds.\n\n{prompt}" if image
            else prompt)
    args = ["claude", "-p", full, "--model", model, "--output-format", "json"]
    if image:
        args += ["--allowedTools", "Read"]
    proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    out = json.loads(proc.stdout)
    text = out["result"]
    model_id = ",".join(out.get("modelUsage", {}).keys())
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(text[:200])
    return json.loads(m.group(0)), model_id


def read(key: str, src: Path, cache: Cache, which: str, model: str = "sonnet") -> None:
    """which = 'subject' or 'supports'; cached by key+which."""
    ck = f"{key}#{which}"
    if ck in cache:
        return
    img = opaque(key, src)
    prompt = {"subject": SUBJECT, "subject_only": SUBJECT_ONLY, "supports": SUPPORTS,
              "social": SOCIAL}[which]
    last = ""
    for _ in range(3):
        try:
            ans, mid = _call(prompt, model, img)
            cache.add(ck, {"item": key, "which": which, "model": mid, **ans})
            return
        except Exception as e:  # noqa: BLE001
            last = str(e)
            if "limit" in last.lower():
                raise SystemExit(f"usage limit reached, stopping cleanly: {last[:120]}")
    cache.add(ck, {"item": key, "which": which, "error": last[:200]})


def judge(group: str, ref: str, items: dict[str, str], cache: Cache,
          model: str = "opus") -> None:
    """items: key -> description. Keys are replaced by opaque ids, order shuffled."""
    if group in cache:
        return
    rng = random.Random(group)
    keys = list(items)
    rng.shuffle(keys)
    ids = {k: f"d{secrets.token_hex(3)}" for k in keys}
    body = "\n".join(f"{ids[k]} — {items[k]}" for k in keys)
    ans, mid = _call(JUDGE.replace("{ref}", ref).replace("{items}", body), model)
    back = {k: ans.get(ids[k], {}) for k in keys}
    cache.add(group, {"model": mid, "verdicts": back})
