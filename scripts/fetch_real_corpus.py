#!/usr/bin/env python3
"""E6 — real corpus: the same famous works seen through real supports on Wikimedia Commons.

Steps (each reprenable, polite to the API: >= 2 s between requests, 60 s pause on HTTP 429):

  list    WORKS -> data/real/candidates/<slug>.json : files of the work's category and of its
          subcategories (depth 2), with size, licence, author, description (extmetadata).
  thumbs  small thumbnails (width 200) of the candidates -> data/real/candidates/thumbs/
  sheets  contact sheets of the thumbnails (to look at them and choose) -> data/real/candidates/sheets/
  fetch   files listed in data/real/selection.json -> data/real/images/ at width 960
  manifest  data/real/selection.json + candidates metadata -> data/real/manifest.jsonl

The choice of images and their annotation (support, layers, work_area, note) were done by looking
at every image (Claude, E6); they live in data/real/selection.json, which `manifest` joins with the
Commons metadata.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import httpx

UA = "impressions-research/0.1 (github.com/maribakulj/impressions)"
API = "https://commons.wikimedia.org/w/api.php"
ROOT = Path(__file__).resolve().parents[1] / "data" / "real"
CAND = ROOT / "candidates"
IMAGES = ROOT / "images"
DELAY = 2.0

# slug -> (title, kind, root categories)
WORKS: dict[str, tuple[str, str, list[str]]] = {
    "mona-lisa": ("Léonard de Vinci, La Joconde", "painting", ["Mona Lisa"]),
    "night-watch": ("Rembrandt, La Ronde de nuit", "painting", ["The Night Watch by Rembrandt"]),
    "pearl-earring": ("Vermeer, La Jeune Fille à la perle", "painting", ["Girl with a Pearl Earring by Johannes Vermeer"]),
    "starry-night": ("Van Gogh, La Nuit étoilée", "painting", ["The Starry Night by van Gogh"]),
    "birth-of-venus": ("Botticelli, La Naissance de Vénus", "painting", ["The Birth of Venus (Botticelli)"]),
    "las-meninas": ("Velázquez, Les Ménines", "painting", ["Las Meninas"]),
    "the-kiss": ("Klimt, Le Baiser", "painting", ["The Kiss (Gustav Klimt)"]),
    "arnolfini": ("Van Eyck, Les Époux Arnolfini", "painting", ["The Arnolfini Portrait by Jan van Eyck"]),
    "the-scream": ("Munch, Le Cri (1893, peinture)", "painting", ["The Scream - Edvard Munch, 1893 - (Nasjonalmuseet)", "The Scream by Edvard Munch"]),
    "liberty": ("Delacroix, La Liberté guidant le peuple", "painting", ["La Liberté guidant le peuple (RF 129) by Eugène Delacroix"]),
    "venus-de-milo": ("Vénus de Milo", "sculpture", ["Venus de Milo"]),
    "nike-samothrace": ("Victoire de Samothrace", "sculpture", ["Nike of Samothrace"]),
    "david-michelangelo": ("Michel-Ange, David", "sculpture", ["David by Michelangelo Buonarroti"]),
    "laocoon": ("Laocoon et ses fils", "sculpture", ["Laocoon group"]),
    "nefertiti": ("Buste de Néfertiti", "sculpture", ["Nefertiti bust (Berlin)", "Nefertiti Bust on stamps"]),
    "melencolia": ("Dürer, Melencolia I", "print", ["Melencolia I by Albrecht Dürer"]),
    "great-wave": ("Hokusai, La Grande Vague de Kanagawa", "print", ["The Great Wave off Kanagawa by Katsushika Hokusai"]),
    "rhinoceros": ("Dürer, Le Rhinocéros", "print", ["Dürer's Rhinoceros"]),
    "vitruvian-man": ("Léonard de Vinci, L'Homme de Vitruve", "drawing", ["Vitruvian Man by Leonardo da Vinci"]),
    "praying-hands": ("Dürer, Mains en prière", "drawing", ["Betende Hände (Dürer)"]),
    "knight-death-devil": ("Dürer, Le Chevalier, la Mort et le Diable", "print", ["Knight, Death and the Devil by Albrecht Dürer"]),
    "migrant-mother": ("Dorothea Lange, Migrant Mother", "photograph", ["Migrant Mother by Dorothea Lange"]),
    "le-gras": ("Niépce, Point de vue du Gras", "photograph", ["Point de vue du Gras"]),
}

_last = 0.0

# subcategories holding other artists' works, not the work itself
SUBCAT_EXCLUDE = re.compile(r"cop(y|ies)|after |parod|pastiche|named|style|derivative|replica|"
                            r"cosplay|meme|graffiti|in art\b|inspired|homage|hommage|tattoo|tile|"
                            r"caricature|lego|costume|uploaded|wikidata|text|logo", re.I)


def get(client: httpx.Client, url: str, params: dict | None = None) -> httpx.Response:
    """GET with >= DELAY s between requests and a 60 s pause on 429."""
    global _last, DELAY
    for attempt in range(6):
        wait = DELAY - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        _last = time.monotonic()
        try:
            r = client.get(url, params=params, follow_redirects=True, timeout=120)
        except httpx.HTTPError as e:
            print("  network error", e, file=sys.stderr)
            time.sleep(20)
            continue
        if r.status_code == 429:
            DELAY = min(DELAY * 1.5, 15.0)  # back off for good
            print(f"  429 (retry-after {r.headers.get('retry-after')}), waiting 60 s, delay now {DELAY:.1f} s",
                  str(r.url)[:100], file=sys.stderr)
            time.sleep(60)
            continue
        return r
    raise RuntimeError(f"giving up on {url}")


def api(client: httpx.Client, **params) -> dict:
    params |= {"format": "json", "formatversion": "2"}
    return get(client, API, params).json()


def members(client: httpx.Client, cat: str, kind: str) -> list[str]:
    out, cont = [], {}
    while True:
        d = api(client, action="query", list="categorymembers", cmtitle=f"Category:{cat}",
                cmtype=kind, cmlimit="500", **cont)
        out += [m["title"] for m in d["query"]["categorymembers"]]
        if "continue" not in d:
            return out
        cont = {"cmcontinue": d["continue"]["cmcontinue"]}


def strip(s: str | None) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def imageinfo(client: httpx.Client, titles: list[str]) -> dict[str, dict]:
    out = {}
    for i in range(0, len(titles), 50):
        d = api(client, action="query", prop="imageinfo", titles="|".join(titles[i:i + 50]),
                iiprop="url|size|mime|extmetadata", iiurlwidth="200",
                iiextmetadatafilter="LicenseShortName|Artist|ImageDescription|Credit")
        for p in d["query"]["pages"]:
            if not p.get("imageinfo"):
                continue
            ii = p["imageinfo"][0]
            em = ii.get("extmetadata", {})
            out[p["title"]] = {
                "title": p["title"], "width": ii.get("width"), "height": ii.get("height"),
                "mime": ii.get("mime"), "thumb": ii.get("thumburl"),
                "page": ii.get("descriptionurl"),
                "license": strip(em.get("LicenseShortName", {}).get("value")),
                "author": strip(em.get("Artist", {}).get("value"))[:200],
                "description": strip(em.get("ImageDescription", {}).get("value"))[:300],
            }
    return out


def cmd_list(slugs: list[str]) -> None:
    CAND.mkdir(parents=True, exist_ok=True)
    with httpx.Client(headers={"User-Agent": UA}) as c:
        for slug in slugs or WORKS:
            dest = CAND / f"{slug}.json"
            if dest.exists():
                continue
            title, kind, roots = WORKS[slug]
            files: dict[str, str] = {}
            seen, frontier = set(), [(r, 0) for r in roots]
            while frontier:
                cat, depth = frontier.pop(0)
                if cat in seen:
                    continue
                seen.add(cat)
                for f in members(c, cat, "file"):
                    files.setdefault(f, cat)
                if depth < 2 and len(seen) < 40:
                    for sub in members(c, cat, "subcat"):
                        if not SUBCAT_EXCLUDE.search(sub):
                            frontier.append((sub.removeprefix("Category:"), depth + 1))
                if len(files) >= 800:
                    break
            info = imageinfo(c, list(files))
            rows = [dict(v, category=files[k]) for k, v in info.items()
                    if v["mime"] in ("image/jpeg", "image/png", "image/tiff", "image/webp")]
            dest.write_text(json.dumps({"slug": slug, "categories": sorted(seen), "files": rows},
                                       ensure_ascii=False, indent=1))
            print(slug, len(seen), "categories", len(rows), "files")


SEARCH_NAME = {"birth-of-venus": "Birth of Venus", "the-kiss": "Klimt Kiss", "the-scream": "Munch Scream",
               "david-michelangelo": "David Michelangelo", "laocoon": "Laocoon",
               "praying-hands": "Praying Hands", "rhinoceros": "Dürer Rhinoceros",
               "le-gras": "Niépce", "knight-death-devil": "Knight, Death and the Devil",
               "nike-samothrace": "Victory of Samothrace", "nefertiti": "Nefertiti bust"}
SEARCH_TERMS = ["stamp", "postcard", "book", "magazine", "screen", "poster", "banner",
                "museum visitors", "reproduction"]


def cmd_search(slugs: list[str]) -> None:
    """Full-text search of File: pages (work name + a support word), added to the candidates."""
    with httpx.Client(headers={"User-Agent": UA}) as c:
        for slug in slugs or WORKS:
            p = CAND / f"{slug}.json"
            d = json.loads(p.read_text())
            if d.get("searched"):
                continue
            name = SEARCH_NAME.get(slug, f'"{WORKS[slug][2][0]}"')
            have = {r["title"] for r in d["files"]}
            found: dict[str, str] = {}
            for term in SEARCH_TERMS:
                r = api(c, action="query", list="search", srnamespace="6", srlimit="20",
                        srsearch=f"{name} {term}")
                for h in r.get("query", {}).get("search", []):
                    if h["title"] not in have:
                        found.setdefault(h["title"], f"search:{term}")
            info = imageinfo(c, list(found))
            d["files"] += [dict(v, category=found[k]) for k, v in info.items()
                           if v["mime"] in ("image/jpeg", "image/png", "image/tiff", "image/webp")]
            d["searched"] = True
            p.write_text(json.dumps(d, ensure_ascii=False, indent=1))
            print(slug, "search", len(found))


def key(title: str) -> str:
    return hashlib.md5(title.encode()).hexdigest()[:10]


def cmd_thumbs(slugs: list[str], per_work: int = 60) -> None:
    """Thumbnails of candidates whose category or name hints at a support (or all if few)."""
    tdir = CAND / "thumbs"
    tdir.mkdir(parents=True, exist_ok=True)
    with httpx.Client(headers={"User-Agent": UA}) as c:
        for slug in slugs or WORKS:
            rows = json.loads((CAND / f"{slug}.json").read_text())["files"]
            for r in pick_candidates(rows, per_work):
                dest = tdir / f"{slug}-{key(r['title'])}.jpg"
                if dest.exists() or not r["thumb"]:
                    continue
                resp = get(c, r["thumb"])
                if resp.status_code == 200:
                    dest.write_bytes(resp.content)
            print(slug, "thumbs done")


HINTS = re.compile(r"louvre|museum|musée|museo|gallery|galer|visitor|crowd|tourist|room|salle|"
                   r"book|livre|page|magazine|stamp|timbre|postcard|poster|affiche|banner|screen|"
                   r"phone|replica|frame|cadre|exhib|in situ|reproduction|print|selfie|display|"
                   r"vitrine|showcase|hall|saal|sala|in the|at the", re.I)
EXCLUDE = re.compile(r"parod|pastiche|graffiti|cosplay|lego|meme|caricature|detail|ausschnitt|"
                     r"dettaglio|détail|x-ray|infrared|cake|tattoo|tile|copy by|copie|kopie", re.I)


def pick_candidates(rows: list[dict], n: int) -> list[dict]:
    rows = [r for r in rows if not EXCLUDE.search(r["title"] + " " + r["category"])]
    hinted = [r for r in rows if HINTS.search(r["title"] + " " + r["category"] + " " + r["description"])]
    rest = [r for r in rows if r not in hinted]
    # deterministic: spread over the list
    out = hinted[:: max(1, len(hinted) // (n - 10))][: n - 10] if len(hinted) > n - 10 else hinted
    step = max(1, len(rest) // max(1, n - len(out)))
    out += rest[::step][: n - len(out)]
    return out


def cmd_sheets(slugs: list[str]) -> None:
    from PIL import Image, ImageDraw
    sdir = CAND / "sheets"
    sdir.mkdir(parents=True, exist_ok=True)
    for slug in slugs or WORKS:
        rows = json.loads((CAND / f"{slug}.json").read_text())["files"]
        cells = []
        for r in pick_candidates(rows, 60):
            p = CAND / "thumbs" / f"{slug}-{key(r['title'])}.jpg"
            if p.exists():
                cells.append((p, r["title"]))
        cols, cw, ch = 8, 200, 190
        sheet = Image.new("RGB", (cols * cw, ((len(cells) + cols - 1) // cols) * ch), "white")
        d = ImageDraw.Draw(sheet)
        index = []
        for i, (p, t) in enumerate(cells):
            try:
                im = Image.open(p).convert("RGB")
            except Exception:
                continue
            im.thumbnail((cw - 6, ch - 22))
            x, y = (i % cols) * cw, (i // cols) * ch
            sheet.paste(im, (x + 3, y + 3))
            d.text((x + 3, y + ch - 18), str(i), fill="red")
            index.append({"i": i, "title": t})
        sheet.save(sdir / f"{slug}.jpg", quality=85)
        (sdir / f"{slug}.json").write_text(json.dumps(index, ensure_ascii=False, indent=0))
        print(slug, len(cells))


def cmd_fetch() -> None:
    sel = json.loads((ROOT / "selection.json").read_text())
    IMAGES.mkdir(parents=True, exist_ok=True)
    with httpx.Client(headers={"User-Agent": UA}) as c:
        for s in sel:
            dest = IMAGES / s["file"]
            if dest.exists():
                continue
            name = s["title"].removeprefix("File:")
            url = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
                   + urllib.parse.quote(name) + "?width=960")
            r = get(c, url)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
                dest.write_bytes(r.content)
                print("ok", s["file"], len(r.content) // 1024, "KB")
            else:
                print("FAIL", r.status_code, name, file=sys.stderr)


def cmd_manifest() -> None:
    sel = json.loads((ROOT / "selection.json").read_text())
    meta = {}
    for slug in WORKS:
        p = CAND / f"{slug}.json"
        if p.exists():
            for r in json.loads(p.read_text())["files"]:
                meta[r["title"]] = r
    with open(ROOT / "manifest.jsonl", "w") as f:
        for s in sel:
            if s.get("drop"):
                continue
            m = meta[s["title"]]
            title, kind, _ = WORKS[s["work"]]
            f.write(json.dumps({
                "file": s["file"], "work": s["work"], "work_title": title,
                "work_kind": s.get("work_kind", kind), "commons_page": m["page"],
                "license": m["license"], "author": m["author"], "support": s["support"],
                "layers": s["layers"], "n_layers": s.get("n_layers", len(s["layers"]) - 1),
                "work_area": s["work_area"], "note": s["note"],
            }, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"list": cmd_list, "search": cmd_search, "thumbs": cmd_thumbs, "sheets": cmd_sheets}[cmd](args) \
        if cmd in ("list", "search", "thumbs", "sheets") else {"fetch": cmd_fetch, "manifest": cmd_manifest}[cmd]()
