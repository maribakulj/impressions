#!/usr/bin/env python3
"""Figure — what Claude names as the subject, stage by stage (E5), with the area control."""

import json

import matplotlib.pyplot as plt

d = json.load(open("results/E5/claude.json"))["stages"]
rows = [("frame|1", "cadre doré"), ("wall|2", "mur (2 couches)"),
        ("book|2", "livre photographié (2)"), ("web|2", "écran (2)"),
        ("print|2", "trame + rephoto (2)"), ("deep|4", "chaîne profonde, 4 couches"),
        ("deep|6", "chaîne profonde, 6 couches"),
        ("match|deep|6", "témoin : même surface que 6, sans couche")]
cats = [("same", "même sujet", "#2a78d6"), ("partial", "partiel", "#1baf7a"),
        ("support", "le support à la place du sujet", "#eb6834"), ("other", "autre sujet", "#eda100")]
fig, ax = plt.subplots(figsize=(9, 4.6), dpi=150)
for y, (key, label) in enumerate(rows):
    left = 0
    for c, name, col in cats:
        n = d[key]["subject_verdicts"].get(c, 0)
        if n:
            ax.barh(y, n - 0.15, left=left, color=col, height=0.62, edgecolor="none")
            if n >= 3:
                ax.text(left + n / 2, y, str(n), ha="center", va="center", fontsize=9,
                        color="white" if c in ("same", "support") else "#222")
        left += n
ax.set_yticks(range(len(rows)), [r[1] for r in rows], fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, 30)
ax.set_xlabel("œuvres (sur 30)", fontsize=9, color="#555")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.axhline(6.5, color="#bbb", lw=0.8, ls=(0, (3, 3)))
handles = [plt.Rectangle((0, 0), 1, 1, color=col) for _, _, col in cats]
ax.legend(handles, [n for _, n, _ in cats], ncol=4, frameon=False, fontsize=8.5,
          loc="lower center", bbox_to_anchor=(0.42, 1.0))
ax.set_title("Ce que Claude dit que l'image représente, couche après couche",
             fontsize=11, loc="left", pad=26)
fig.tight_layout()
fig.savefig("article/figures/fig-sujet-support.png")
