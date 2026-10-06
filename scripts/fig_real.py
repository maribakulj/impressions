#!/usr/bin/env python3
"""Figure 3 — 149 real reproductions (blind readings): share where the work is the main subject,
only named, or recognised (answer to 'which artwork?'), by annotated number of layers."""

import json

import matplotlib.pyplot as plt

d = json.load(open("results/E10b/blind.json"))
labels = ["0-1", "2", "3", "4+"]
main = [d["real"][f"layers {l}"]["main"] for l in labels]
named = [d["real"][f"layers {l}"]["named"] for l in labels]
rec = [d["artwork_recognised"][f"real|layers {l}"]["share"] for l in labels]
n = [d["real"][f"layers {l}"]["n"] for l in labels]
x = range(len(labels))
fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=150)
for vals, lab, col in [(rec, "œuvre reconnue (« quelle œuvre ? »)", "#1baf7a"),
                       (named, "œuvre nommée dans la description", "#86b6ef"),
                       (main, "œuvre sujet principal de la description", "#2a78d6")]:
    ax.errorbar(x, [v[0] for v in vals], yerr=[[v[0] - v[1] for v in vals], [v[2] - v[0] for v in vals]],
                color=col, marker="o", ms=5, lw=2, capsize=3, label=lab)
ax.set_xticks(list(x), [f"{l} couche{'s' if l != '0-1' else ''}\n(n = {k})" for l, k in zip(labels, n)],
              fontsize=8.5)
ax.set_ylim(-0.03, 1.05)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.grid(axis="y", color="#e5e5e5", lw=0.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=8, loc="lower left")
ax.set_title("149 vraies reproductions de 22 œuvres (lectures à l'aveugle)", fontsize=10.5,
             loc="left")
fig.tight_layout()
fig.savefig("article/figures/fig-reel.png")
