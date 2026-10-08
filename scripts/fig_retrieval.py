#!/usr/bin/env python3
"""Figure 2 — encoders (E4 v2, images completed to a square): share of works found in the top
ten among 18 405 images, for the photographed book and its three matched-area controls."""

import json

import matplotlib.pyplot as plt

rows = [("match|book|2", "seule, centrée, même surface"),
        ("degr|book|2", "mêmes pixels, même place, sur gris"),
        ("book|2", "dans un livre photographié"),
        ("clut|book|2", "centrée sur un autre tableau")]
models = [("clip", "CLIP"), ("siglip", "SigLIP"), ("dinov2", "DINOv2")]
colors = {"book|2": "#eb6834"}
fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), dpi=150, sharey=True)
for ax, (m, name) in zip(axes, models):
    st = json.load(open(f"results/E4/{m}.json"))["stages"]
    for y, (k, _) in enumerate(rows):
        v, lo, hi = st[k]["self_top10"]
        col = colors.get(k, "#2a78d6")
        ax.plot([lo, hi], [y, y], color=col, lw=2, solid_capstyle="round")
        ax.plot(v, y, "o", color=col, ms=8, mec="white", mew=1.5)
        ax.text(hi + 0.03, y, f"{v:.0%}", va="center", fontsize=8.5, color="#222")
    ax.set_title(name, fontsize=10, loc="left")
    ax.set_xlim(0, 0.8)
    ax.set_xticks([0, 0.25, 0.5, 0.75])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.grid(axis="x", color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
axes[0].set_yticks(range(len(rows)), [r[1] for r in rows], fontsize=9)
axes[0].invert_yaxis()
axes[1].set_xlabel("œuvre retrouvée dans les 10 premiers (sur 18 405 images ; 300 œuvres, IC 95 %)",
                   fontsize=8.5, color="#555")
fig.suptitle("Retrouver l'œuvre à surface égale : tout entourage la dilue, un autre tableau plus qu'un livre",
             fontsize=10.5, x=0.01, ha="left")
fig.tight_layout()
fig.savefig("article/figures/fig-retrouver.png")
