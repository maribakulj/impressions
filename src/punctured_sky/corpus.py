"""Read-only access to the museum pool built by caypollard (never written to)."""

from __future__ import annotations

import json
from pathlib import Path

CAYPOLLARD = Path.home() / "caypollard"
MANIFEST = CAYPOLLARD / "data/derived/museums-v0.2/manifest.jsonl"

# Wikidata classes for the object types compared in this project
TYPES = {
    "Q3305213": "painting",
    "Q11060274": "print",
    "Q93184": "drawing",
    "Q860861": "sculpture",
    "Q125191": "photograph",
}


def load_pool() -> list[dict]:
    rows = []
    with MANIFEST.open() as fh:
        for line in fh:
            row = json.loads(line)
            row["image_abspath"] = str(CAYPOLLARD / row["image_path"])
            kinds = [TYPES[t] for t in row.get("type", []) if t in TYPES]
            row["kind"] = kinds[0] if kinds else "other"
            rows.append(row)
    return rows


def load_works(path: str | Path = "data/works.jsonl") -> list[dict]:
    """The sampled works, with ``image_abspath`` resolved against the caypollard checkout."""
    rows = []
    with open(path) as fh:
        for line in fh:
            row = json.loads(line)
            row["image_abspath"] = str(CAYPOLLARD / row["image_path"])
            rows.append(row)
    return rows
