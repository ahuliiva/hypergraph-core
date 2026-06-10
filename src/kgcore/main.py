from pathlib import Path
import tempfile

from kgcore.algorithms.peeling import PeelingAlgorithm
from kgcore.datasets.adapters import WeightedIncidenceCsvAdapter
from kgcore.types import CoreParams


SAMPLE_CSV = """edge_id,vertex_id,edge_weight,vertex_weight
E1,A,2.0,1.0
E1,B,2.0,0.8
E2,B,1.5,0.8
E2,C,1.5,1.1
E3,C,0.7,1.1
E3,D,0.7,0.9
"""


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        csv_path = Path(tmp_dir) / "sample.csv"
        csv_path.write_text(SAMPLE_CSV, encoding="utf-8")

        adapter = WeightedIncidenceCsvAdapter()
        hypergraph = adapter.load(csv_path)

        algorithm = PeelingAlgorithm()
        result = algorithm.run(hypergraph, CoreParams(k=1))

        print("Vertices:", sorted(result.remaining_vertices))
        print("Edges:", sorted(result.remaining_edges))
        print("Vertex weights:", hypergraph.vertex_weights())
        print("Edge weights:", hypergraph.edge_weights())


if __name__ == "__main__":
    main()