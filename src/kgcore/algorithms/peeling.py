from kgcore.algorithms.base import CoreAlgorithm
from kgcore.hypergraph import Hypergraph
from kgcore.types import CoreParams, CoreResult


class PeelingAlgorithm(CoreAlgorithm):
    def run(self, hypergraph: Hypergraph, params: CoreParams) -> CoreResult:
        remaining_vertices = set(hypergraph.vertices())

        changed = True
        while changed:
            changed = False
            to_remove = {
                v
                for v in remaining_vertices
                if self._degree_in_subset(hypergraph, v, remaining_vertices) < params.k
            }
            if to_remove:
                remaining_vertices.difference_update(to_remove)
                changed = True

        remaining_edges = {
            edge_id
            for edge_id, edge_vertices in hypergraph.edges().items()
            if edge_vertices.issubset(remaining_vertices)
        }

        return CoreResult(
            remaining_vertices=remaining_vertices,
            remaining_edges=remaining_edges,
            metadata={"algorithm": "peeling", "k": params.k},
        )

    @staticmethod
    def _degree_in_subset(hypergraph: Hypergraph, vertex: str, allowed_vertices: set[str]) -> int:
        count = 0
        for edge_id in hypergraph.incident_edges(vertex):
            if hypergraph.edge_vertices(edge_id).issubset(allowed_vertices):
                count += 1
        return count