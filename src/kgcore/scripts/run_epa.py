# scripts/run_nashville.py
from pathlib import Path
from kgcore.datasets.adapters import RsvpAdapter
from kgcore.algorithms.epa import EPA
from kgcore.algorithms.epa2 import EPA2
from kgcore.types import CoreParams

from tqdm import tqdm
import tracemalloc
import time

def main() -> None:
    hypergraph = RsvpAdapter().load(Path("data/rsvps.csv"))

    print(f"Вершин: {len(hypergraph.vertices())}")
    print(f"Гиперрёбер: {len(hypergraph.edges())}")

    # result = PeelingAlgorithm().run(hypergraph, CoreParams(k=2))
    # print(f"k=2 core: {len(result.remaining_vertices)} вершин")


    epa = EPA2(hypergraph)
    start = time.perf_counter()
    epa_result = epa.compute(5,5)
    print(f"\EPA2 calculated in  {time.perf_counter() - start:.8f}s")

    epa = EPA2(hypergraph)
    tracemalloc.start()
    epa_result = epa.compute(5,5)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Пиковая память: {peak / 1024 / 1024:.4f} MB")




    epa = EPA(hypergraph)
    start = time.perf_counter()
    epa_result = epa.compute(5,5)
    print(f"\EPA calculated in  {time.perf_counter() - start:.8f}s")

    epa = EPA(hypergraph)
    tracemalloc.start()
    epa_result = epa.compute(5,5)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Пиковая память: {peak / 1024 / 1024:.4f} MB")




if __name__ == "__main__":
    main()