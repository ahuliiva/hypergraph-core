from collections import defaultdict
from pathlib import Path

from kgcore.datasets.base import DatasetAdapter
from kgcore.datasets.csv_readers import read_csv_rows
from kgcore.hypergraph import Hypergraph, WeightedHypergraph


class IncidenceCsvAdapter(DatasetAdapter):
    def load(self, path: Path) -> Hypergraph:
        rows = read_csv_rows(path)
        grouped: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            grouped[row["edge_id"]].add(row["vertex_id"])

        hypergraph = Hypergraph()
        for edge_id, vertices in grouped.items():
            hypergraph.add_edge(edge_id, vertices)
        return hypergraph


class WeightedIncidenceCsvAdapter(DatasetAdapter):
    def load(self, path: Path) -> WeightedHypergraph:
        rows = read_csv_rows(path)
        grouped: dict[str, set[str]] = defaultdict(set)
        edge_weights: dict[str, float] = {}
        vertex_weights: dict[str, float] = {}

        for row in rows:
            edge_id = row["edge_id"]
            vertex_id = row["vertex_id"]
            grouped[edge_id].add(vertex_id)

            edge_weight = row.get("edge_weight")
            if edge_weight not in (None, ""):
                edge_weights[edge_id] = float(edge_weight)

            vertex_weight = row.get("vertex_weight")
            if vertex_weight not in (None, ""):
                vertex_weights[vertex_id] = float(vertex_weight)

        hypergraph = WeightedHypergraph()
        for edge_id, vertices in grouped.items():
            hypergraph.add_edge(edge_id, vertices, weight=edge_weights.get(edge_id))

        for vertex_id, weight in vertex_weights.items():
            if vertex_id in hypergraph.vertices():
                hypergraph.set_vertex_weight(vertex_id, weight)

        return hypergraph
    

class RsvpAdapter(DatasetAdapter):
#   Загружает Nashville Meetup rsvps.csv.
#     Каждое событие (event_id) → гиперребро,
#     каждый участник (member_id) → вершина.
    def load(self, path: Path) -> Hypergraph:
        rows = read_csv_rows(path)
        grouped: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            grouped[row["event_id"]].add(row["member_id"])

        hypergraph = Hypergraph()
        for edge_id, vertices in grouped.items():
            hypergraph.add_edge(edge_id, vertices)
        return hypergraph