#!/usr/bin/env python3
"""E2 — one sheet per layer over five works of different types, to look before measuring."""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

from PIL import Image

from punctured_sky.corpus import load_works
from punctured_sky.layers import LAYERS
from punctured_sky.sheets import contact_sheet


def main() -> None:
    works = load_works()
    rng = random.Random(7)
    pick = []
    for kind in ["painting", "print", "drawing", "sculpture", "photograph"]:
        pick.append(rng.choice([w for w in works if w["kind"] == kind]))
    names = sys.argv[1:] or list(LAYERS)
    items = []
    for name in names:
        for i, w in enumerate(pick):
            im = Image.open(w["image_abspath"])
            items.append((LAYERS[name](im, random.Random(i)), f"{name}\n{w['kind']}"))
    Path("figures").mkdir(exist_ok=True)
    out = f"figures/E2-layers-{'-'.join(names) if sys.argv[1:] else 'all'}.jpg"
    contact_sheet(items, cols=5, cell=300).save(out, quality=85)
    print(out)


if __name__ == "__main__":
    main()
