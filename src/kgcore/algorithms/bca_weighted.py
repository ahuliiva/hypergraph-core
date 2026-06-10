# src/kgcore/algorithms/bca_weighted.py
from __future__ import annotations
from collections import defaultdict, deque
from enum import Enum
from kgcore.hypergraph import WeightedHypergraph


class SupportMode(Enum):
    UNWEIGHTED    = "unweighted"     # базовый: количество общих рёбер
    EDGE_WEIGHT   = "edge_weight"    # сумма весов общих рёбер
    VERTEX_WEIGHT = "vertex_weight"  # min(w(u), w(v)) * количество общих рёбер
    COMBINED      = "combined"       # сумма w(e) * min(w(u), w(v))


class BCA_weighted:
    def __init__(self, hypergraph: WeightedHypergraph, mode: SupportMode = SupportMode.EDGE_WEIGHT) -> None:
        self.G = hypergraph
        self.mode = mode
        self._support_cache: dict[tuple[str, str], float] = {}
        self.k_cores: dict[tuple[int, int], set[str]] = {}
        self.coreness: dict[tuple[int, int], set[str]] = {}

    def compute_support(self, u: str, v: str) -> float:
        """s(u,v) — взвешенная поддержка, формула зависит от mode."""
        key = (min(u, v), max(u, v))
        if key in self._support_cache:
            return self._support_cache[key]

        common_edges = self.G.incident_edges(u) & self.G.incident_edges(v)

        match self.mode:
            case SupportMode.UNWEIGHTED:
                result = float(len(common_edges))

            case SupportMode.EDGE_WEIGHT:
                # s(u,v) = сумма весов общих рёбер
                # смысл: если встречи были "значимые" (большой RSVPs count),
                # поддержка выше
                result = sum(
                    self.G.edge_weight(e, default=1.0)
                    for e in common_edges
                )

            case SupportMode.VERTEX_WEIGHT:
                # s(u,v) = min(w(u), w(v)) * кол-во общих рёбер
                # смысл: поддержка ограничена менее активной вершиной
                wu = self.G.vertex_weight(u, default=1.0)
                wv = self.G.vertex_weight(v, default=1.0)
                result = min(wu, wv) * len(common_edges)

            case SupportMode.COMBINED:
                # s(u,v) = min(w(u), w(v)) * сумма весов общих рёбер
                # смысл: и активность вершин, и значимость событий
                wu = self.G.vertex_weight(u, default=1.0)
                wv = self.G.vertex_weight(v, default=1.0)
                result = min(wu, wv) * sum(
                    self.G.edge_weight(e, default=1.0)
                    for e in common_edges
                )

        self._support_cache[key] = result
        return result

    def get_g_neighbors(self, v: str, g: float, active: set[str]) -> set[str]:
        return {u for u in active if u != v and self.compute_support(v, u) >= g}

    def compute(self, g_step: float = 1.0) -> dict[tuple[int, int], set[str]]:
        """
        g теперь может быть вещественным (для взвешенных режимов).
        g_step — шаг перебора значений g.
        """
        D: dict[tuple[int, int], set[str]] = {}
        g = g_step
        g_idx = 1  # целочисленный индекс для ключей D[(k, g_idx)]

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
                    D[(k, g_idx)] = active.copy()
                    self.k_cores[(k, g_idx)] = active.copy()

            g += g_step
            g_idx += 1

        self.coreness = self._deduplication(self.k_cores)
        return D

    def _deduplication(self, D):
        result = {}
        for (k, g), H in D.items():
            V1 = H.copy()
            if h1 := D.get((k + 1, g)):
                V1 -= h1
            if h2 := D.get((k, g + 1)):
                V1 -= h2
            if V1:
                result[(k, g)] = V1
        return result