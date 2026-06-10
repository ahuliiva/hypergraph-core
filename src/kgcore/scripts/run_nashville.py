# scripts/run_nashville.py
from pathlib import Path
from kgcore.datasets.adapters import RsvpAdapter
from kgcore.algorithms.peeling import PeelingAlgorithm
from kgcore.algorithms.bca import BCA
from kgcore.types import CoreParams
import time
from tqdm import tqdm


def main() -> None:
    hypergraph = RsvpAdapter().load(Path("data/rsvps.csv"))
    print(f"\ncalculating support for all>> ")
    start = time.perf_counter()
    sup = hypergraph.support_index
    print(f"\nsupport calculated:  {time.perf_counter() - start:.8f}s")

    print(f"Вершин: {len(hypergraph.vertices())}")
    print(f"Гиперрёбер: {len(hypergraph.edges())}")

    result = PeelingAlgorithm().run(hypergraph, CoreParams(k=2))
    print(f"PeelingAlgorithm k=2 core: {len(result.remaining_vertices)} вершин")

    # hypergraph = RsvpAdapter().load(Path("data/rsvps.csv"))

    print(f"\nBCA init..")
    bca = BCA(hypergraph)
    print(f"\nBCA compute")
    start = time.perf_counter()
    bca_result = bca.compute()
    print(f"\nBCA calculated in  {time.perf_counter() - start:.8f}s")
    
    print(f"BCA result size: {len(bca_result)}")
    print(f"BCA coreness: {bca.coreness}")




if __name__ == "__main__":
    main()