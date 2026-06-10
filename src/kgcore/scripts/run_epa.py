# scripts/run_nashville.py
from pathlib import Path
from kgcore.datasets.adapters import RsvpAdapter
from kgcore.algorithms.peeling import PeelingAlgorithm
from kgcore.types import CoreParams

def main() -> None:
    hypergraph = RsvpAdapter().load(Path("data/rsvps.csv"))

    print(f"Вершин: {len(hypergraph.vertices())}")
    print(f"Гиперрёбер: {len(hypergraph.edges())}")

    result = PeelingAlgorithm().run(hypergraph, CoreParams(k=2))
    print(f"k=2 core: {len(result.remaining_vertices)} вершин")

    

if __name__ == "__main__":
    main()