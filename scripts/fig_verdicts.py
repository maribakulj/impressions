#!/usr/bin/env python3
"""Figure 1 — round 2 (subject asked alone, blind): share of descriptions where the work is the
main subject, for the same work in eight situations at matched area."""

import json

import matplotlib.pyplot as plt

d = json.load(open("results/E10c/round2.json"))["conditions"]
rows = [("degr", "mêmes pixels, même place, sur gris"),
        ("match", "seule, centrée, même surface"),
        ("wall", "encadrée, accrochée au mur"),
        ("clut", "centrée sur un autre tableau"),
        ("book_notext", "dans un livre photographié, sans texte"),
        ("book", "dans un livre photographié"),
        ("web", "dans une page web, sur un écran"),
        ("degclut", "mêmes pixels, même place, sur un autre tableau")]
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150)
for y, (k, label) in enumerate(rows):
    v = d[k]
    col = "#2a78d6" if k in ("degr", "match", "wall") else "#eb6834"
    ax.barh(y, max(v["main"], 0.004), color=col, height=0.62)
    lo, hi = v["main_ci"]
    ax.errorbar(v["main"], y, xerr=[[v["main"] - lo], [hi - v["main"]]], color="#333",
                capsize=3, lw=1.1)
    ax.text(hi + 0.02, y, f"{v['main']:.0%}", va="center", fontsize=9, color="#222")
ax.set_yticks(range(len(rows)), [r[1] for r in rows], fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, 1.12)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.set_xlabel("l'œuvre est le sujet principal de la description (30 œuvres, à l'aveugle)",
              fontsize=8.5, color="#555")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.suptitle("La même œuvre, à surface égale : ce qui compte, c'est ce qui l'entoure",
             fontsize=10.5, x=0.01, ha="left")
fig.tight_layout()
fig.savefig("article/figures/fig-sujet-support.png")
