#!/usr/bin/env python3
"""E10b — analysis of the blind readings (replaces e5_analyse.py and the hand counts of E6).

Subject (judge, Opus, blind): per condition, share of descriptions where the work's subject is
named at all, and share where it is the main subject (vs. a complement of something else).
Layers (H3): Spearman with average ranks, against two baselines (always 1; a rule that knows
the condition), and within each condition. Real (E6): logistic regression of 'not main subject'
on annotated layers + log10(area) + in-situ, bootstrap grouped by work. All intervals: 95 %,
bootstrap over works (2 000 draws) or Wilson for single proportions.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

rng = np.random.default_rng(0)


def wilson(k: int, n: int) -> list[float]:
    if n == 0:
        return [float("nan")] * 3
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [p, max(0, c - h), min(1, c + h)]


def grouped_boot(groups: dict[str, list[float]], n: int = 2000) -> list[float]:
    keys = list(groups)
    vals = [np.mean([x for k in keys for x in groups[k]])]
    for _ in range(n):
        pick = rng.choice(keys, len(keys))
        vals.append(np.mean([x for k in pick for x in groups[k]]))
    return [float(vals[0]), float(np.percentile(vals[1:], 2.5)),
            float(np.percentile(vals[1:], 97.5))]


def logit_fit(X, y, iters=50):
    w = np.zeros(X.shape[1])
    for _ in range(iters):  # Newton–Raphson with a small ridge for separable resamples
        p = 1 / (1 + np.exp(-X @ w))
        g = X.T @ (y - p) - 1e-3 * w
        H = -(X.T * (p * (1 - p))) @ X - 1e-3 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w


def main() -> None:
    reads = {}
    for l in open("data/annotations/blind_readings.jsonl"):
        r = json.loads(l)
        if "error" not in r:
            reads.setdefault(r["item"], {})[r["which"]] = r
    verdict = {}
    for l in open("data/annotations/blind_judged.jsonl"):
        verdict.update(json.loads(l)["verdicts"])
    existing = {json.loads(l)["key"]: json.loads(l)["n_layers"]
                for l in open("data/annotations/existing_layers.jsonl")}
    manifest = {json.loads(l)["file"]: json.loads(l) for l in open("data/real/manifest.jsonl")}
    out = {"synthetic": {}, "screens": {}, "real": {}}

    # --- synthetic and screens: subject by condition
    by_cond = defaultdict(lambda: defaultdict(lambda: {"named": [], "main": []}))
    for item, v in verdict.items():
        kind, work, cond, k = item.split("|")[0], item.split("|")[1], "|".join(item.split("|")[2:-1]), item.split("|")[-1]
        if kind == "real":
            continue
        key = f"{cond}|{k}"
        g = by_cond[(kind, key)][work]
        g["named"].append(float(bool(v.get("named"))))
        g["main"].append(float(v.get("role") == "main"))
    for (kind, key), groups in sorted(by_cond.items()):
        named = {w: d["named"] for w, d in groups.items()}
        main = {w: d["main"] for w, d in groups.items()}
        n = sum(len(x) for x in named.values())
        out["synthetic" if kind == "syn" else "screens"][key] = {
            "n": n, "named": grouped_boot(named), "main": grouped_boot(main)}

    # --- layers counted (H3), synthetic
    pred, truth_add, truth_all, cond = [], [], [], []
    for item, r in reads.items():
        if not item.startswith("syn|") or "supports" not in r:
            continue
        _, work, c, k = item.split("|")[0], item.split("|")[1], "|".join(item.split("|")[2:-1]), int(item.split("|")[-1])
        try:
            p = float(r["supports"]["n_layers"])
        except (TypeError, ValueError):
            continue
        added = k if not c.startswith(("match", "degr", "clut")) else 0
        pred.append(p), truth_add.append(added), truth_all.append(added + existing[work])
        cond.append(f"{c}|{k}")
    pred, truth_add, truth_all, cond = map(np.array, (pred, truth_add, truth_all, cond))
    informed = np.array([truth_all[cond == c].mean() for c in cond])
    h3 = {}
    for name, t in (("added", truth_add), ("added+existing", truth_all)):
        h3[name] = {"spearman": float(spearmanr(pred, t).statistic),
                    "mae": float(np.abs(pred - t).mean()),
                    "mae_always_1": float(np.abs(1 - t).mean()),
                    "mae_condition_rule": float(np.abs(informed - t).mean()),
                    "within_one": float((np.abs(pred - t) <= 1).mean())}
    h3["within_condition_spearman_vs_existing"] = {
        c: float(spearmanr(pred[cond == c], truth_all[cond == c]).statistic)
        for c in sorted(set(cond)) if np.std(truth_all[cond == c]) > 0 and np.std(pred[cond == c]) > 0}
    h3["synthetic_flag"] = {c: float(np.mean([bool(reads[i]["supports"].get("synthetic"))
                                              for i in reads if i.startswith("syn|") and "supports" in reads[i]
                                              and f"{'|'.join(i.split('|')[2:-1])}|{i.split('|')[-1]}" == c]))
                            for c in sorted(set(cond))}
    out["synthetic_layers"] = h3

    # --- real
    rows = []
    for item, v in verdict.items():
        if not item.startswith("real|"):
            continue
        f = item.split("|")[2]
        a = manifest[f]
        rows.append({"work": a["work"], "layers": a["n_layers"],
                     "area": max(a["work_area"], 0.005), "in_situ": a["support"] == "in_situ",
                     "named": bool(v.get("named")), "main": v.get("role") == "main",
                     "support": a["support"]})
    X = lambda rs: np.column_stack([np.ones(len(rs)), [r["layers"] for r in rs],
                                    np.log10([r["area"] for r in rs]), [r["in_situ"] for r in rs]])
    y = lambda rs: np.array([0.0 if r["main"] else 1.0 for r in rs])
    works = sorted({r["work"] for r in rows})
    point = logit_fit(X(rows), y(rows))
    boots = []
    for _ in range(2000):
        pick = rng.choice(works, len(works))
        rs = [r for w in pick for r in rows if r["work"] == w]
        boots.append(logit_fit(X(rs), y(rs)))
    boots = np.array(boots)
    out["real"]["logit_not_main"] = {
        name: [float(point[i]), *np.percentile(boots[:, i], [2.5, 97.5]).tolist()]
        for i, name in enumerate(["intercept", "layers", "log10_area", "in_situ"])}
    for lab, sel in [("0-1", lambda r: r["layers"] <= 1), ("2", lambda r: r["layers"] == 2),
                     ("3", lambda r: r["layers"] == 3), ("4+", lambda r: r["layers"] >= 4)]:
        rs = [r for r in rows if sel(r)]
        out["real"][f"layers {lab}"] = {"n": len(rs),
                                        "named": wilson(sum(r["named"] for r in rs), len(rs)),
                                        "main": wilson(sum(r["main"] for r in rs), len(rs))}
    rr = [(it, r) for it, r in reads.items() if it.startswith("real|") and "supports" in r]
    try:
        p = np.array([float(r["supports"]["n_layers"]) for _, r in rr])
        t = np.array([manifest[it.split("|")[2]]["n_layers"] for it, _ in rr])
        out["real"]["layers_counted"] = {"spearman": float(spearmanr(p, t).statistic),
                                         "mae": float(np.abs(p - t).mean()),
                                         "mae_mean_rule": float(np.abs(t - t.mean()).mean()),
                                         "within_one": float((np.abs(p - t) <= 1).mean())}
        out["real"]["synthetic_flag"] = float(np.mean([bool(r["supports"].get("synthetic")) for _, r in rr]))
    except (TypeError, ValueError):
        pass
    # --- second judgment: is the work recognised in the answer to 'which artwork?'
    art = {}
    for l in open("data/annotations/blind_judged_artwork.jsonl"):
        art.update(json.loads(l)["verdicts"])
    by = defaultdict(lambda: defaultdict(list))
    for item, v in art.items():
        parts = item.split("|")
        kind, work = parts[0], parts[1]
        key = f"{'|'.join(parts[2:-1])}|{parts[-1]}" if kind == "syn" else None
        if kind == "real":
            a = manifest[parts[2]]
            n = a["n_layers"]
            key = "layers " + ("0-1" if n <= 1 else str(n) if n < 4 else "4+")
        by[(kind, key)][work].append(float(bool(v.get("named"))))
    out["artwork_recognised"] = {f"{k}|{key}": {"share": grouped_boot(g),
                                                "n": sum(len(x) for x in g.values())}
                                 for (k, key), g in sorted(by.items())}
    Path("results/E10b").mkdir(parents=True, exist_ok=True)
    json.dump(out, open("results/E10b/blind.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
