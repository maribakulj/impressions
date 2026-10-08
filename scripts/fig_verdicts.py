#!/usr/bin/env python3
"""Figure 1 — round 2 (subject asked alone, blind): for the same 30 works in eight situations at
matched area, is the work's subject the main subject of the description, a complement, or left
out? (Codex review: omission and subordination are shown apart.)"""

import json

import matplotlib.pyplot as plt

d = json.load(open("results/E10c/round2.json"))["conditions"]
rows = [("degr", "mêmes pixels, même place, sur gris"),
        ("match", "seule, centrée, même surface"),
        ("wall", "encadrée, accrochée au mur"),
        ("clut", "centrée sur un autre tableau"),
        ("book_notext2", "dans un livre photographié, sans texte"),
        ("book", "dans un livre photographié"),
        ("web", "dans une page web, sur un écran"),
        ("degclut", "mêmes pixels, même place, sur un autre tableau")]
parts = [("main", "sujet principal", "#2a78d6", "white"),
         ("complement", "complément", "#f2b48a", "#3a2a1e"),
         ("absent", "absent", "#d4d4d4", "#333")]
fig, ax = plt.subplots(figsize=(9, 4.4), dpi=150)
for y, (k, label) in enumerate(rows):
    v, left = d[k], 0.0
    for key, _, col, ink in parts:
        n = v[key]
        if n:
            ax.barh(y, n - 0.15, left=left, color=col, height=0.64)
            if n >= 2:
                ax.text(left + n / 2, y, str(n), ha="center", va="center", fontsize=8.5,
                        color=ink)
        left += n
ax.set_yticks(range(len(rows)), [r[1] for r in rows], fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, 30)
ax.set_xticks([0, 10, 20, 30])
ax.set_xlabel("nombre de descriptions sur 30 œuvres (sujet demandé seul, lecture et jugement à l'aveugle)",
              fontsize=8.5, color="#555")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c, _ in parts]
ax.legend(handles, [p[1] for p in parts], ncol=3, frameon=False, fontsize=8.5,
          loc="lower left", bbox_to_anchor=(0, 1.0))
fig.suptitle("Le sujet de l'œuvre dans la description : ce qui compte, c'est ce qui l'entoure",
             fontsize=10.5, x=0.01, ha="left")
fig.tight_layout()
fig.savefig("article/figures/fig-sujet-support.png")
