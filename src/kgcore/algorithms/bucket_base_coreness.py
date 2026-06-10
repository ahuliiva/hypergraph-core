# BucketBasedCoreness — альтернативная реализация с явным перебором (k,g)
from __future__ import annotations
from kgcore.hypergraph import Hypergraph


class BucketBasedCoreness:
    def __init__(self, hypergraph: Hypergraph) -> None:
        self.G = hypergraph
        self._support_cache: dict[tuple[str, str], int] = {}
        self.k_cores: dict[tuple[int, int], set[str]] = {}

    def compute_support(self, u: str, v: str) -> int:
        key = (min(u, v), max(u, v))
        if key not in self._support_cache:
            self._support_cache[key] = len(
                self.G.incident_edges(u) & self.G.incident_edges(v)
            )
        return self._support_cache[key]

    def _compute_k_g_core(self, k: int, g: int, active: set[str]) -> set[str]:
        g_neighbor_count = {
            v: sum(1 for u in active if u != v and self.compute_support(v, u) >= g)
            for v in active
        }
        max_count = max(g_neighbor_count.values(), default=0)
        buckets: list[set[str]] = [set() for _ in range(max_count + 1)]
        for v, count in g_neighbor_count.items():
            buckets[count].add(v)

        to_remove = set().union(*buckets[:k])
        while to_remove:
            active -= to_remove
            for v in active:
                count = sum(
                    1 for u in active if u != v and self.compute_support(v, u) >= g
                )
                g_neighbor_count[v] = count
            new_buckets: list[set[str]] = [set() for _ in range(max_count + 1)]
            for v in active:
                idx = min(g_neighbor_count[v], max_count)
                new_buckets[idx].add(v)
            buckets = new_buckets
            to_remove = set().union(*buckets[:k])
        return active

    def compute_all_cores(self, max_k: int | None = None, max_g: int | None = None) -> None:
        if max_k is None:
            max_k = max((self.G.degree(v) for v in self.G.vertices()), default=0)
        if max_g is None:
            max_g = max((len(self.G.incident_edges(v)) for v in self.G.vertices()), default=0)
        for g in range(1, max_g + 1):
            for k in range(max_k + 1):
                core = self._compute_k_g_core(k, g, self.G.vertices())
                if core:
                    self.k_cores[(k, g)] = core

    def get_k_g_core(self, k: int, g: int) -> set[str] | None:
        return self.k_cores.get((k, g))