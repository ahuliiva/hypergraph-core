from kgcore.hypergraph import Hypergraph
from kgcore.algorithms import BCA


def create_example_hypergraph() -> Hypergraph:
    edges = [
        {1, 2, 3, 4},       # e0
        {1, 3, 4, 5},       # e1
        {5, 6, 7, 8},       # e2
        {6, 7, 8, 9, 10},   # e3
        {8, 9, 11},         # e4
    ]
    return Hypergraph.from_edge_list(edges)




def test() -> None:

    G = create_example_hypergraph()

    bca = BCA(G)

    print("\nBCA!!!")
    D = bca.compute()

    print("\nВсе (k,g)-core:")
    for (k, g), core in sorted(D.items()):
        print(f"  (k={k}, g={g}): {sorted(core)}")

    print("\nВсе (k,g)-короа:")
    for (k, g), core in sorted(bca.k_cores.items()):
        print(f"  (k={k}, g={g}): {sorted(core)}")


    D_dedup = bca.coreness

    print("\nВсе dedup (k,g)-core:")
    for (k, g), core in sorted(D_dedup.items()):
        print(f"  (k={k}, g={g}): {sorted(core)}")