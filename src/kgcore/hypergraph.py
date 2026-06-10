from __future__ import annotations


class Hypergraph:
    def __init__(self) -> None:
        self._vertices: set[str] = set()
        self._edges: dict[str, frozenset[str]] = {}
        self._incident: dict[str, set[str]] = {}

    @classmethod
    def from_edge_list(
        cls,
        edges: list[list[str] | set[str] | frozenset[str]],
    ) -> "Hypergraph":
        """
        Создаёт гиперграф из списка гиперрёбер.
        edge_id назначается автоматически: e0, e1, e2, ...

        Пример:
            H = Hypergraph.from_edge_list([
                {1, 2, 3, 4},
                {1, 3, 4, 5},
            ])
        """
        g = cls()
        for i, edge in enumerate(edges):
            g.add_edge(f"e{i}", {str(v) for v in edge})
        return g

    def add_vertex(self, vertex: str) -> None:
        self._vertices.add(vertex)
        self._incident.setdefault(vertex, set())

    def add_edge(self, edge_id: str, vertices: list[str] | set[str] | frozenset[str]) -> None:
        verts = frozenset(vertices)
        if not verts:
            raise ValueError("Hyperedge must contain at least one vertex")
        self._edges[edge_id] = verts
        for vertex in verts:
            self.add_vertex(vertex)
            self._incident[vertex].add(edge_id)

    def vertices(self) -> set[str]:
        return set(self._vertices)

    def edges(self) -> dict[str, frozenset[str]]:
        return dict(self._edges)

    def edge_vertices(self, edge_id: str) -> frozenset[str]:
        return self._edges[edge_id]

    def incident_edges(self, vertex: str) -> set[str]:
        return set(self._incident.get(vertex, set()))

    def degree(self, vertex: str) -> int:
        return len(self._incident.get(vertex, set()))

    def edge_size(self, edge_id: str) -> int:
        return len(self._edges[edge_id])

    def induced_subgraph(self, vertices: set[str]) -> "Hypergraph":
        subgraph = self.__class__()
        for edge_id, edge_vertices in self._edges.items():
            remaining = edge_vertices.intersection(vertices)
            if remaining:
                if isinstance(self, WeightedHypergraph) and isinstance(subgraph, WeightedHypergraph):
                    subgraph.add_edge(edge_id, remaining, weight=self.edge_weight(edge_id, default=None))
                else:
                    subgraph.add_edge(edge_id, remaining)
        if isinstance(self, WeightedHypergraph) and isinstance(subgraph, WeightedHypergraph):
            for vertex in subgraph.vertices():
                weight = self.vertex_weight(vertex, default=None)
                if weight is not None:
                    subgraph.set_vertex_weight(vertex, weight)
        return subgraph


class WeightedHypergraph(Hypergraph):
    def __init__(self) -> None:
        super().__init__()
        self._vertex_weights: dict[str, float] = {}
        self._edge_weights: dict[str, float] = {}

    def add_edge(
        self,
        edge_id: str,
        vertices: list[str] | set[str] | frozenset[str],
        weight: float | None = None,
    ) -> None:
        super().add_edge(edge_id, vertices)
        if weight is not None:
            self._edge_weights[edge_id] = float(weight)

    def set_vertex_weight(self, vertex: str, weight: float) -> None:
        if vertex not in self._vertices:
            raise KeyError(f"Unknown vertex: {vertex}")
        self._vertex_weights[vertex] = float(weight)

    def set_edge_weight(self, edge_id: str, weight: float) -> None:
        if edge_id not in self._edges:
            raise KeyError(f"Unknown edge: {edge_id}")
        self._edge_weights[edge_id] = float(weight)

    def vertex_weight(self, vertex: str, default: float | None = 1.0) -> float | None:
        return self._vertex_weights.get(vertex, default)

    def edge_weight(self, edge_id: str, default: float | None = 1.0) -> float | None:
        return self._edge_weights.get(edge_id, default)

    def vertex_weights(self) -> dict[str, float]:
        return dict(self._vertex_weights)

    def edge_weights(self) -> dict[str, float]:
        return dict(self._edge_weights)
