#!/usr/bin/env python3
"""Figure 1 — blind readings: is the work's subject the main subject of Claude's description,
or only named as a complement? Synthetic stages and their three same-area controls (E10b)."""

import json

import matplotlib.pyplot as plt

d = json.load(open("results/E10b/blind.json"))
syn, art = d["synthetic"], d["artwork_recognised"]
rows = [("frame|1", "cadre doré"), ("wall|2", "mur (2 couches)"),
        ("web|2", "page web → écran (2)"), ("book|2", "livre photographié (2)"),
        ("match|book|2", "  témoin : même surface"), ("degr|book|2", "  témoin : même dégradation"),
        ("clut|book|2", "  témoin : entourée, non contenue")]
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150)
for y, (key, label) in enumerate(rows):
    main, named = syn[key]["main"], syn[key]["named"]
    rec = art.get(f"syn|{key}", {}).get("share", [float("nan")])[0]
    ax.barh(y, named[0], color="#b7d3f6", height=0.62)
    ax.barh(y, main[0], color="#2a78d6", height=0.62)
    ax.errorbar(main[0], y, xerr=[[main[0] - main[1]], [main[2] - main[0]]], color="#0d366b",
                capsize=3, lw=1.2)
    ax.text(1.02, y, f"reconnue {rec:.0%}", va="center", fontsize=8.5, color="#444")
ax.set_yticks(range(len(rows)), [r[1] for r in rows], fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.axhline(3.5, color="#bbb", lw=0.8, ls=(0, (3, 3)))
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
handles = [plt.Rectangle((0, 0), 1, 1, color="#2a78d6"), plt.Rectangle((0, 0), 1, 1, color="#b7d3f6")]
ax.legend(handles, ["l'œuvre est le sujet principal de la description",
                    "l'œuvre est seulement nommée (complément)"], ncol=2, frameon=False,
          fontsize=8.5, loc="lower center", bbox_to_anchor=(0.45, 1.0))
ax.set_title("Lectures à l'aveugle de 30 œuvres : reconnue, mais rétrogradée par le support",
             fontsize=10.5, loc="left", pad=24)
fig.tight_layout()
fig.savefig("article/figures/fig-sujet-support.png")
