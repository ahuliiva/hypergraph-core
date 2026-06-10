# src/kgcore/algorithms/bca.py
from __future__ import annotations
from collections import defaultdict, deque
from typing import Optional
from kgcore.hypergraph import Hypergraph
from tqdm import tqdm


class BCA:
    """Bucket-based Coreness Algorithm — полная (k,g)-декомпозиция."""

    def __init__(self, hypergraph: Hypergraph) -> None:
        self.G = hypergraph
        self._support_cache: dict[tuple[str, str], int] = {}
        self.k_cores: dict[tuple[int, int], set[str]] = {}
        self.coreness: dict[tuple[int, int], set[str]] = {}
        # self.precompute_all_supports()

    def compute_support(self, u: str, v: str) -> int:
        key = (min(u, v), max(u, v))
        return self.G.support_index.get(key, 0)
    

    # def get_g_neighbors(self, v: str, g: int, active: set[str]) -> set[str]:
    #     return {u for u in active if u != v and self.compute_support(v, u) >= g}
    
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

    def compute(self) -> dict[tuple[int, int], set[str]]:
        D: dict[tuple[int, int], set[str]] = {}

        max_g = max(self.G.support_index.values(), default=0)
        print(f"max_g = {max_g}, всего итераций: {max_g}")
        prev_active = set(self.G.vertices())
        g = 1
        while True:
            buckets: dict[int, set[str]] = defaultdict(set)
            g_neighbor_count: dict[str, int] = {}
            active: set[str] = set()

            seed = prev_active.copy()
            nuum = len(seed)
            print(f"\ng={g} число вершин: {nuum} ")
            
            
            for v in tqdm(seed, desc=f"g={g}"):
                nbrs = self.get_g_neighbors(v, g, seed)
                if nbrs:
                    g_neighbor_count[v] = len(nbrs)
                    buckets[len(nbrs)].add(v)
                    active.add(v)

            # print(f"\nactive size: {len(active)}")
            
            if not active:
                break

            k = 0
            while active:
                k += 1
                # print(f"\nk={k}, active size: {len(active)}")
                queue = deque(v for j, s in buckets.items() if j < k for v in s)
                # print(f"\nqueue size: {len(queue)}")
                while queue:
                    v = queue.pop()
                    if v not in active:
                        continue
                    nbrs = self.get_g_neighbors(v, g, active)
                    active.discard(v)
                    # print(f"\n discard {v}, active size: {len(active)}")
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
            # max_core_for_this_g — вершины с максимальным k при данном g
            # это те что выжили дольше всего = active последнего непустого k
            # в D[(k_max, g)] уже записан правильный результат
            # для следующей итерации берём объединение всех core при этом g:
            prev_active = set.union(*[v for (ki, gi), v in D.items() if gi == g], set())
            # print(f"\nprev_active : {prev_active}")
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
    

    # def precompute_all_supports(self) -> None:
    #     for edge_id, verts in self.G.edges().items():
    #         verts_list = list(verts)
    #         w_e = (
    #             self.G.edge_weight(edge_id, default=1.0)
    #             if isinstance(self.G, Hypergraph)
    #             else 1.0
    #         )
    #         for i in range(len(verts_list)):
    #             for j in range(i + 1, len(verts_list)):
    #                 key = (min(verts_list[i], verts_list[j]),
    #                     max(verts_list[i], verts_list[j]))
    #                 self._support_cache[key] = (
    #                     self._support_cache.get(key, 0.0) + w_e
    #             )
    

    