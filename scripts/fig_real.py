#!/usr/bin/env python3
"""Figure — real reproductions (E6): what Claude names as the subject, by number of layers."""

import json
from collections import Counter

import matplotlib.pyplot as plt

m = {json.loads(l)["file"]: json.loads(l) for l in open("data/real/manifest.jsonl")}
V = {}
for l in open("data/annotations/e6_judged.jsonl"):
    V.update(json.loads(l)["verdicts"])
groups = {"0-1 couche": Counter(), "2 couches": Counter(), "3 couches": Counter(),
          "4 couches et plus": Counter()}
for f, v in V.items():
    n = m[f]["n_layers"]
    g = "0-1 couche" if n <= 1 else "2 couches" if n == 2 else "3 couches" if n == 3 else "4 couches et plus"
    groups[g][v] += 1
cats = [("same", "même sujet", "#2a78d6"), ("partial", "partiel", "#1baf7a"),
        ("support", "le support ou la scène à la place du sujet", "#eb6834"),
        ("other", "autre sujet", "#eda100")]
fig, ax = plt.subplots(figsize=(9, 3.2), dpi=150)
for y, (g, c) in enumerate(groups.items()):
    total, left = sum(c.values()), 0
    for key, _, col in cats:
        share = c.get(key, 0) / total
        if share:
            ax.barh(y, share - 0.004, left=left, color=col, height=0.6)
            if c[key] >= 3:
                ax.text(left + share / 2, y, str(c[key]), ha="center", va="center", fontsize=9,
                        color="white" if key in ("same", "support") else "#222")
        left += share
    ax.text(1.01, y, f"n = {total}", va="center", fontsize=8.5, color="#555")
ax.set_yticks(range(len(groups)), list(groups), fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
handles = [plt.Rectangle((0, 0), 1, 1, color=col) for _, _, col in cats]
ax.legend(handles, [n for _, n, _ in cats], ncol=4, frameon=False, fontsize=8,
          loc="lower center", bbox_to_anchor=(0.45, 1.0))
ax.set_title("149 vraies reproductions de 22 œuvres (hors images de référence) : ce que Claude dit qu'elles représentent",
             fontsize=10.5, loc="left", pad=24)
fig.tight_layout()
fig.savefig("article/figures/fig-reel.png")
