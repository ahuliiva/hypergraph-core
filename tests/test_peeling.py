from kgcore.algorithms.peeling import PeelingAlgorithm
from kgcore.hypergraph import Hypergraph
from kgcore.types import CoreParams


def test_peeling_k1_keeps_all_vertices() -> None:
    h = Hypergraph()
    h.add_edge("E1", ["A", "B"])
    h.add_edge("E2", ["B", "C"])

    result = PeelingAlgorithm().run(h, CoreParams(k=1))

    assert result.remaining_vertices == {"A", "B", "C"}
    assert result.remaining_edges == {"E1", "E2"}


def test_peeling_k2_removes_non_core_vertices() -> None:
    h = Hypergraph()
    h.add_edge("E1", ["A", "B"])
    h.add_edge("E2", ["B", "C"])

    result = PeelingAlgorithm().run(h, CoreParams(k=2))

    assert result.remaining_vertices == set()
    assert result.remaining_edges == set()