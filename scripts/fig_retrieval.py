#!/usr/bin/env python3
"""Figure — retrieving the work through the deep chain, against the same-area control (E4)."""

import json

import matplotlib.pyplot as plt

MODELS = [("clip", "CLIP"), ("siglip", "SigLIP"), ("dinov2", "DINOv2")]
LAYERS = ["", "cadre doré", "mur", "page", "livre photographié", "page web", "écran"]
fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), dpi=150, sharey=True)
for ax, (m, name) in zip(axes, MODELS):
    d = json.load(open(f"results/E4/{m}.json"))["stages"]
    for prefix, label, col in [("deep", "dans les couches", "#2a78d6"),
                               ("match|deep", "seule, même surface", "#eb6834")]:
        xs, ys, lo, hi = [0], [d["orig|0"]["self_top10"][0]], [0], [0]
        for k in range(1, 7):
            v = d[f"{prefix}|{k}"]["self_top10"]
            xs.append(k), ys.append(v[0]), lo.append(v[0] - v[1]), hi.append(v[2] - v[0])
        ax.errorbar(xs, ys, yerr=[lo, hi], color=col, lw=2, marker="o", ms=5, capsize=2,
                    label=label)
    ax.set_title(name, fontsize=10, loc="left")
    ax.set_xticks(range(7))
    ax.set_xticklabels([str(k) for k in range(7)], fontsize=8)
    ax.set_xlabel("couches ajoutées", fontsize=8.5, color="#555")
    ax.set_ylim(-0.03, 1.03)
    ax.grid(axis="y", color="#e5e5e5", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
axes[0].set_ylabel("œuvre retrouvée dans les 10 premiers\n(sur 18 405 images)", fontsize=8.5)
axes[0].legend(frameon=False, fontsize=8.5, loc="upper right")
fig.suptitle("Retrouver l'œuvre : cadre doré → mur → page → livre photographié → page web → écran",
             fontsize=10.5, x=0.01, ha="left")
fig.tight_layout()
fig.savefig("article/figures/fig-retrouver.png")
