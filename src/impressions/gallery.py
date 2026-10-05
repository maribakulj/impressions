"""The search gallery: the pool embeddings of one model, with labels for scoring neighbours."""

from __future__ import annotations

import numpy as np

from impressions.corpus import load_pool


class Gallery:
    def __init__(self, model: str):
        data = np.load(f"data/cache/pool-{model}.npz")
        self.ids = list(data["ids"])
        self.vecs = data["vecs"].astype(np.float32)
        self.vecs /= np.linalg.norm(self.vecs, axis=1, keepdims=True) + 1e-8
        self.index = {i: k for k, i in enumerate(self.ids)}
        pool = {r["id"]: r for r in load_pool()}
        self.rows = [pool[i] for i in self.ids]

    def neighbours(self, q: np.ndarray, k: int = 10, exclude: str | None = None):
        sims = self.vecs @ q
        if exclude is not None and exclude in self.index:
            sims[self.index[exclude]] = -np.inf
        top = np.argpartition(-sims, k)[:k]
        top = top[np.argsort(-sims[top])]
        return [(self.rows[t], float(sims[t])) for t in top]

    def rank_of(self, q: np.ndarray, target: str) -> int:
        """1-based rank of the work itself (its museum image) among the gallery."""
        sims = self.vecs @ q
        return int((sims > sims[self.index[target]]).sum()) + 1
