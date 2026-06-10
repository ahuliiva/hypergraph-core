# src/kgcore/algorithms/bca.py
from __future__ import annotations
from collections import defaultdict, deque
from typing import Optional
from kgcore.hypergraph import Hypergraph


class BCA:
    """Bucket-based Coreness Algorithm — полная (k,g)-декомпозиция."""

    def __init__(self, hypergraph: Hypergraph) -> None:
        self.G = hypergraph
        self._support_cache: dict[tuple[str, str], int] = {}
        self.k_cores: dict[tuple[int, int], set[str]] = {}
        self.coreness: dict[tuple[int, int], set[str]] = {}

    def compute_support(self, u: str, v: str) -> int:
        key = (min(u, v), max(u, v))
        if key not in self._support_cache:
            self._support_cache[key] = len(
                self.G.incident_edges(u) & self.G.incident_edges(v)
            )
        return self._support_cache[key]

    def get_g_neighbors(self, v: str, g: int, active: set[str]) -> set[str]:
        return {u for u in active if u != v and self.compute_support(v, u) >= g}

    def compute(self) -> dict[tuple[int, int], set[str]]:
        D: dict[tuple[int, int], set[str]] = {}
        g = 1
        while True:
            buckets: dict[int, set[str]] = defaultdict(set)
            g_neighbor_count: dict[str, int] = {}
            active: set[str] = set()

            for v in self.G.vertices():
                nbrs = self.get_g_neighbors(v, g, self.G.vertices())
                if nbrs:
                    g_neighbor_count[v] = len(nbrs)
                    buckets[len(nbrs)].add(v)
                    active.add(v)

            if not active:
                break

            k = 0
            while active:
                k += 1
                queue = deque(v for j, s in buckets.items() if j < k for v in s)
                while queue:
                    v = queue.pop()
                    if v not in active:
                        continue
                    nbrs = self.get_g_neighbors(v, g, active)
                    active.discard(v)
                    buckets[g_neighbor_count[v]].discard(v)
                    for w in nbrs:
                        if w in active and w not in queue:
                            buckets[g_neighbor_count[w]].discard(w)
                            g_neighbor_count[w] -= 1
                            if g_neighbor_count[w] < k:
                                queue.append(w)
                            buckets[g_neighbor_count[w]].add(w)
                if active:
                    D[(k, g)] = active.copy()
                    self.k_cores[(k, g)] = active.copy()
            g += 1

        self.coreness = self._deduplication(self.k_cores)
        return D

    def _deduplication(
        self, D: dict[tuple[int, int], set[str]]
    ) -> dict[tuple[int, int], set[str]]:
        result: dict[tuple[int, int], set[str]] = {}
        for (k, g), H in D.items():
            V1 = H.copy()
            if h1 := D.get((k + 1, g)):
                V1 -= h1
            if h2 := D.get((k, g + 1)):
                V1 -= h2
            if V1:
                result[(k, g)] = V1
        return result