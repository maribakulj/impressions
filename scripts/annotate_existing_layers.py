#!/usr/bin/env python3
"""E3 — which layers does each 'original' museum image already carry?

The museum photograph is never the bare object (JOURNAL, E1): frames, mounts, sheet edges,
studio backgrounds are already there. Claude reads each of the 300 images and lists them.
"""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor

from punctured_sky.claude_vision import Cache, ask_json
from punctured_sky.corpus import load_works

PROMPT = """Cette image est la reproduction numérique d'un objet de musée. Je ne te demande PAS
ce qu'elle représente. Je te demande quelles « couches » entourent l'objet dans cette image,
c'est-à-dire tout ce qui n'est pas l'œuvre elle-même mais la présente, l'encadre ou la supporte.

Réponds uniquement par un objet JSON avec ces clés (booléens sauf indication) :
- "picture_frame": un cadre (moulure, baguette) est visible autour de l'œuvre
- "mount_or_card": l'œuvre est collée ou posée sur un carton, un montage, un passe-partout
- "sheet_edges": on voit les bords de la feuille de papier (marges, bords irréguliers)
- "inscriptions_outside": du texte, des cachets, des numéros hors de l'image (marge, montage)
- "studio_background": l'objet est détouré sur un fond de studio uni (gris, blanc, noir)
- "plinth_or_support": un socle, un support, une main, un présentoir est visible
- "room_or_wall": on voit une salle, un mur, un sol
- "binding_or_book": on voit une reliure, un livre, un album, une couverture
- "glass_or_reflection": vitre, reflet, éclat lumineux
- "color_chart_or_ruler": mire de couleur, réglette, échelle
- "cropped_object": l'objet est coupé par le bord de l'image
- "n_layers": nombre entier de couches distinctes que tu comptes entre l'objet et le bord de
  l'image (0 si l'objet occupe toute l'image sans rien autour)
- "note": une phrase courte en français décrivant ces couches
"""


def main(limit: int | None = None) -> None:
    works = load_works()[:limit]
    cache = Cache("data/annotations/existing_layers.jsonl")
    todo = [w for w in works if w["id"] not in cache]
    print(len(todo), "to annotate", flush=True)

    def one(w):
        try:
            ans = ask_json(w["image_abspath"], PROMPT)
            cache.add(w["id"], {"kind": w["kind"], **ans})
            return w["id"], "ok"
        except Exception as e:  # noqa: BLE001 - logged and retried on the next run
            return w["id"], f"error {e}"[:200]

    with ThreadPoolExecutor(3) as ex:
        for i, (wid, status) in enumerate(ex.map(one, todo)):
            print(i, wid, status, flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
