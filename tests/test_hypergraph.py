from kgcore.hypergraph import Hypergraph, WeightedHypergraph


def test_hypergraph_basic_operations() -> None:
    h = Hypergraph()
    h.add_edge("E1", ["A", "B"])
    h.add_edge("E2", ["B", "C"])

    assert h.vertices() == {"A", "B", "C"}
    assert h.degree("B") == 2
    assert h.edge_size("E1") == 2


def test_weighted_hypergraph_supports_vertex_and_edge_weights() -> None:
    h = WeightedHypergraph()
    h.add_edge("E1", ["A", "B"], weight=2.5)
    h.set_vertex_weight("A", 1.2)

    assert h.edge_weight("E1") == 2.5
    assert h.vertex_weight("A") == 1.2
    assert h.vertex_weight("B") == 1.0