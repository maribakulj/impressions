#!/usr/bin/env python3
"""Social round (pilot) — what the frame and the room do to indirect readings (Claude Sonnet,
blind; subject answers judged blind by Claude Haiku). Writes results/social/pilot.json."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import median

ITEMS = json.loads(Path("data/social/items.json").read_text())
MUSEUM = re.compile(r"musée|galerie|exposition|collection|collectionneur|salle d'art|antiquaire|vente aux enchères", re.I)
INSTIT = re.compile(r"musée|collection|collectionneur|institution|fondation|galerie|antiquaire|maison de vente", re.I)


def price(v) -> float | None:
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"\d[\d\s.,]*", str(v) or "")
    if not m:
        return None
    s = m.group(0).replace(" ", "").replace(" ", "")
    s = s.replace(",", ".") if s.count(",") == 1 and len(s.split(",")[1]) <= 2 else s.replace(",", "")
    try:
        return float(s.rstrip("."))
    except ValueError:
        return None


def load(source: str = "claude") -> dict:
    rows = {}
    if source == "claude":
        R = defaultdict(dict)
        for l in open("data/annotations/social_readings.jsonl"):
            r = json.loads(l)
            R[r["item"]][r["which"]] = r
        J = {}
        for l in open("data/annotations/social_judged.jsonl"):
            r = json.loads(l)
            J[r["key"]] = r
        for it in ITEMS["items"]:
            k = f"soc|{it['content']}|{it['frame']}|{it['space']}"
            rows[k] = {**it, "subject": R[k]["subject_only"].get("subject"), "social": R[k]["social"],
                       "judge": J.get(k, {})}
    return rows


def summarise(rows: dict) -> dict:
    out = {}
    for dim in ("frame", "space"):
        g = defaultdict(list)
        for r in rows.values():
            g[r[dim]].append(r)
        out[f"by_{dim}"] = {}
        for k, rs in g.items():
            soc = [r["social"] for r in rs]
            out[f"by_{dim}"][k] = {
                "n": len(rs),
                "subject_main": sum(r["judge"].get("role") == "main" for r in rs) / len(rs),
                "described_as_artwork": sum(bool(r["judge"].get("as_artwork")) for r in rs) / len(rs),
                "frame_mentioned": sum(bool(r["judge"].get("frame_mentioned")) for r in rs) / len(rs),
                "art_oui": sum(str(s.get("art", "")).lower().startswith("oui") for s in soc) / len(rs),
                "art_non": sum(str(s.get("art", "")).lower().startswith("non") for s in soc) / len(rs),
                "place_museum": sum(bool(MUSEUM.search(str(s.get("lieu", "")))) for s in soc) / len(rs),
                "owner_institution": sum(bool(INSTIT.search(str(s.get("proprietaire", "")))) for s in soc) / len(rs),
            }
    # price: only where the work is the main thing in view (grey, gallery), per content x frame
    pr = defaultdict(dict)
    for r in rows.values():
        if r["space"] in ("grey", "gallery"):
            pr[r["content"]].setdefault(r["frame"], []).append(price(r["social"].get("prix_euros")))
    out["price_median_grey_gallery"] = {c: {f: median([x for x in v if x is not None]) if any(
        x is not None for x in v) else None for f, v in d.items()} for c, d in pr.items()}
    # content x frame, isolated (grey + gallery): described as an artwork, place read as museum
    cf = defaultdict(lambda: defaultdict(list))
    for r in rows.values():
        if r["space"] in ("grey", "gallery"):
            cf[r["content"]][r["frame"]].append(r)
    out["content_by_frame_isolated"] = {c: {f: {
        "as_artwork": sum(bool(x["judge"].get("as_artwork")) for x in rs),
        "place_museum": sum(bool(MUSEUM.search(str(x["social"].get("lieu", "")))) for x in rs),
        "owner_institution": sum(bool(INSTIT.search(str(x["social"].get("proprietaire", "")))) for x in rs),
        "n": len(rs)} for f, rs in d.items()} for c, d in cf.items()}
    return out


def main() -> None:
    rows = load()
    out = summarise(rows)
    Path("results/social").mkdir(parents=True, exist_ok=True)
    json.dump(out, open("results/social/pilot.json", "w"), indent=1, ensure_ascii=False)
    for dim in ("frame", "space"):
        print(f"\n== par {dim} (n par case)")
        keys = ["subject_main", "described_as_artwork", "frame_mentioned", "art_oui", "art_non",
                "place_museum", "owner_institution"]
        print(f"{'':10s}" + "".join(f"{k[:14]:>15s}" for k in keys))
        for k, v in out[f"by_{dim}"].items():
            print(f"{k:10s}" + "".join(f"{v[x]:15.2f}" for x in keys) + f"   n={v['n']}")
    print("\n== prix médian (gris + galerie), par contenu et cadre")
    for c, d in out["price_median_grey_gallery"].items():
        print(f"{c:9s}", {f: d[f] for f in ITEMS["frames"]})
    print("\n== isolé (gris + galerie, 2 images par case) : œuvre / lieu musée / propriétaire institution")
    for c, d in out["content_by_frame_isolated"].items():
        print(f"{c:9s}", "  ".join(f"{f}:{d[f]['as_artwork']}/{d[f]['place_museum']}/{d[f]['owner_institution']}" for f in ITEMS["frames"]))


if __name__ == "__main__":
    main()
