# src/kgcore/algorithms/epa.py
from __future__ import annotations
from collections import deque
from kgcore.hypergraph import Hypergraph


class EPA2:
    """Efficient Peeling Algorithm для вычисления (k,g)-core."""

    def __init__(self, hypergraph: Hypergraph) -> None:
        self.G = hypergraph
        # self._support_cache: dict[tuple[str, str], int] = {}

    def compute_support(self, u: str, v: str) -> int:
        key = (min(u, v), max(u, v))
        return self.G.support_index.get(key, 0)

    def get_g_neighbors(self, v: str, g: int, active: set[str]) -> set[str]:
        candidates: set[str] = set()
        for e in self.G.incident_edges(v):
            candidates |= self.G.edge_vertices(e)
        candidates.discard(v)
        candidates &= active  # только живые
        return {
            u for u in candidates
            if self.G.support_index.get((min(u, v), max(u, v)), 0) >= g
        }
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