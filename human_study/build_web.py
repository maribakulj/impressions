#!/usr/bin/env python3
"""Build the web version of the human study (human_study/web/index.html): the same 72 images,
6 lists and questions as form.html, with, after the last image, what each image was and what
Claude said of it (round 2, subject asked alone) with the blind judge's verdict."""

import csv
import json
from pathlib import Path

TITLES = {  # Wikidata labels, fetched 08/10/2026
    "Q112181476": ("Baptême du Christ", "Veit Stoss"),
    "Q116377829": ("La Résurrection", ""),
    "Q17334826": ("Portrait de femme, peut-être Lucretia Boudaen", "Jacob van Loo"),
    "Q18338569": ("L'Adoration des rois mages", "Albrecht Dürer"),
    "Q20201879": ("Vierge à l'Enfant debout", ""),
    "Q21727631": ("Les Noces de Cana", "Benvenuto Tisi, dit le Garofalo"),
    "Q41449677": ("Rue aux Saintes-Maries-de-la-Mer", "Vincent van Gogh"),
    "Q59590707": ("Tête de saint, d'après Fra Angelico", "Edgar Degas"),
    "Q96181868": ("Sphacelaria filicina (algue)", ""),
    "Q97733002": ("Le Général La Fayette… prend la Lune avec les dents", ""),
    "Q97767981": ("The Times, planche 1", "William Hogarth"),
    "Q97788707": ("John Bull observant la comète", "Thomas Rowlandson"),
}
CONDITIONS = {
    "degr": "les pixels de l'œuvre tels qu'ils sont dans le livre photographié, à la même place, sur du gris",
    "degclut": "les mêmes pixels, à la même place, sur le détail d'un autre tableau",
    "book": "l'œuvre reproduite dans un livre ouvert, photographié sur une table",
    "book_notext2": "le même livre photographié, même géométrie, sans aucun texte",
    "web": "l'œuvre dans une page web de musée, photographiée sur un écran",
    "wall": "l'œuvre encadrée, accrochée au mur d'une salle",
}
KIND = {"painting": "peinture", "print": "estampe", "drawing": "dessin",
        "sculpture": "sculpture", "photograph": "photographie"}
ROLE = {"main": "sujet principal", "complement": "complément", "absent": "absent"}


def main() -> None:
    root = Path(__file__).parent
    reads = {}
    for line in open("data/annotations/blind2_readings.jsonl"):
        r = json.loads(line)
        if r.get("which") == "subject_only":
            reads[r["item"]] = r["subject"]
    verdicts = {}
    for line in open("data/annotations/blind2b_judged.jsonl"):
        for item, v in json.loads(line)["verdicts"].items():
            verdicts[item] = v.get("role") if v.get("named") else "absent"
    items = []
    for row in csv.DictReader(open(root / "items.csv")):
        q = row["work"].split(":")[1]
        key = f"r2|{row['work']}|{row['condition']}|0"
        title, creator = TITLES[q]
        items.append({"image": row["image"], "list": int(row["list"]), "work": q,
                      "title": title, "creator": creator, "kind": KIND[row["kind"]],
                      "condition": row["condition"], "conditionLabel": CONDITIONS[row["condition"]],
                      "claude": reads[key], "claudeRole": ROLE[verdicts[key]]})
    lists = json.loads((root / "lists.json").read_text())
    data = {"lists": lists, "items": {it["image"]: it for it in items}}
    tpl = (root / "web_template.html").read_text()
    (root / "web" / "index.html").write_text(
        tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    print(len(items), "items,", len(lists), "lists")


if __name__ == "__main__":
    main()
