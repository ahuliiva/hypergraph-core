# src/kgcore/algorithms/epa.py
from __future__ import annotations
from collections import deque
from kgcore.hypergraph import Hypergraph


class EPA:
    """Efficient Peeling Algorithm для вычисления (k,g)-core."""

    def __init__(self, hypergraph: Hypergraph) -> None:
        self.G = hypergraph
        self._support_cache: dict[tuple[str, str], int] = {}

    def compute_support(self, u: str, v: str) -> int:
        """s(u,v) — количество общих рёбер."""
        key = (min(u, v), max(u, v))
        if key not in self._support_cache:
            edges_u = self.G.incident_edges(u)
            edges_v = self.G.incident_edges(v)
            self._support_cache[key] = len(edges_u & edges_v)
        return self._support_cache[key]

    def get_g_neighbors(self, v: str, g: int, active: set[str]) -> set[str]:
        return {u for u in active if u != v and self.compute_support(v, u) >= g}

    def compute(self, k: int, g: int) -> set[str]:
        active = self.G.vertices()
        g_neighbor_count = {v: len(self.get_g_neighbors(v, g, active)) for v in active}
        queue = deque(v for v in active if g_neighbor_count[v] < k)

        while queue:
            v = queue.popleft()
            neighbors = self.get_g_neighbors(v, g, active)
            active.discard(v)
            for w in neighbors:
                if w in active and w not in queue:
                    g_neighbor_count[w] -= 1
                    if g_neighbor_count[w] < k:
                        queue.append(w)
        return active