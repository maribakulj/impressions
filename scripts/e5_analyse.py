#!/usr/bin/env python3
"""E5 — H3 (counting layers) and H4 (does the named subject survive) from Claude's readings."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from impressions.chains import CHAINS

KIND_FR = {"painting": "peinture", "print": "estampe", "drawing": "dessin",
           "sculpture": "sculpture", "photograph": "photographie"}


def main() -> None:
    reads = [json.loads(l) for l in open("data/annotations/e5_readings.jsonl")]
    existing = {json.loads(l)["key"]: json.loads(l)["n_layers"]
                for l in open("data/annotations/existing_layers.jsonl")}
    judged = {json.loads(l)["key"]: json.loads(l)["verdicts"]
              for l in open("data/annotations/e5_judged.jsonl")}
    rng = np.random.default_rng(0)
    stage_names = list(dict.fromkeys((r["chain_name"], r["k"]) for r in reads))
    out = {"stages": {}}
    pred_all, true_all = [], []
    for name, k in stage_names:
        rows = [r for r in reads if (r["chain_name"], r["k"]) == (name, k) and "error" not in r]
        added = 0 if name == "orig" else (1 if name.startswith("match|") else k)
        true = np.array([existing[r["work"]] + added for r in rows], float)
        pred = np.array([r["n_layers"] for r in rows], float)
        pred_all += list(pred)
        true_all += list(true)
        verdicts = Counter(judged[r["work"]].get(f"{name}:{k}", "orig") for r in rows)
        kind_ok = np.mean([KIND_FR[r["kind"]] in str(r.get("work_kind", "")).lower()
                           for r in rows])
        out["stages"][f"{name}|{k}"] = {
            "n": len(rows),
            "true_layers_mean": float(true.mean()),
            "claude_layers_mean": float(pred.mean()),
            "mae": float(np.abs(pred - true).mean()),
            "synthetic_rate": float(np.mean([bool(r.get("synthetic")) for r in rows])),
            "work_kind_correct": float(kind_ok),
            "subject_verdicts": dict(verdicts),
        }
    p, t = np.array(pred_all), np.array(true_all)
    # trivial baselines: always the mean; always the number of layers *added* (ignores the
    # layers already in the museum image)
    out["counting"] = {
        "spearman": float(np.corrcoef(np.argsort(np.argsort(p)), np.argsort(np.argsort(t)))[0, 1]),
        "mae": float(np.abs(p - t).mean()),
        "mae_constant_baseline": float(np.abs(t - t.mean()).mean()),
        "exact": float((p == t).mean()),
        "within_one": float((np.abs(p - t) <= 1).mean()),
    }
    Path("results/E5").mkdir(parents=True, exist_ok=True)
    json.dump(out, open("results/E5/claude.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out["counting"], indent=1))
    for key, s in out["stages"].items():
        print(f"{key:14s} n={s['n']:2d} vrai={s['true_layers_mean']:.1f} claude="
              f"{s['claude_layers_mean']:.1f} mae={s['mae']:.2f} synth={s['synthetic_rate']:.2f}"
              f" type_ok={s['work_kind_correct']:.2f} sujet={s['subject_verdicts']}")


if __name__ == "__main__":
    main()
