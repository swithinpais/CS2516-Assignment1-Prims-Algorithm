from __future__ import annotations  # for compatibility with older Python versions

import logging
import random
import math
import timeit
import sys
import json

from graph import Graph, Edge, Vertex
from priority_queue import APQ, HeapAPQ, UnsortedListAPQ, Element
from dict_zip import dict_zip

import matplotlib.pyplot as plt


def create_graph(n: int, m: int) -> Graph:
    if m > ((n * (n - 1)) // 2):
        raise ValueError(
            f"Cannot create {m} edges for a graph with {n} nodes.")
    g = Graph()

    vertices = [Vertex("0")]
    g.add_vertex(vertices[0])

    # A set of tuples of all the edges made
    edges: set[tuple[str, str]] = set()

    for i in range(1, n):
        v = Vertex(str(i))

        v2 = random.choice(vertices)

        w = random.randint(1, 20)

        e = Edge(v, v2, w, w)

        edges.add((v.label, v2.label))
        vertices.append(v)

        g.add_vertex(v)
        g.add_edge(v, v2, e)

    for _ in range(m - n + 1):
        # Vertex 0 and Vertex 1 are always connected
        v1, v2 = vertices[0], vertices[1]
        # so the while loop will always run at least once

        while (v1.label, v2.label) in edges or (v2.label, v1.label) in edges:
            # Get two vertices that have not been connected already
            v1, v2 = random.sample(vertices, 2)

        w = random.randint(1, 20)

        e = Edge(v1, v2, w, w)

        edges.add((v1.label, v2.label))
        g.add_edge(v1, v2, e)

    return g


def prim(g: Graph, apq: APQ) -> list[Edge]:
    locs: dict[Vertex, Element] = {}
    for v in g.vertices:
        el = apq.add(math.inf, (v, None))
        locs[v] = el

    tree = []
    while apq.length():
        c: tuple[Vertex, Edge] = apq.remove_min()
        v, e = c
        del locs[v]
        if e is not None:
            tree.append(e)

        for d in g.get_edges(v):
            w = d.opposite(v)
            if w in locs:
                cost = d.weight
                if cost < apq.get_key(locs[w]):
                    locs[w].value = (w, d)
                    apq.update_key(locs[w], cost)
    return tree


def prim_heap(g: Graph) -> list[Edge]:
    apq = HeapAPQ()
    return prim(g, apq)


def prim_unsorted_list(g: Graph) -> list[Edge]:
    apq = UnsortedListAPQ()
    return prim(g, apq)


def time_functions(ratios: list[float], ns: list[int], iterations: int = 100):

    times_heap: dict[int, dict[float, float]] = {}
    times_unsorted_list: dict[int, dict[float, float]] = {}

    for n in ns:
        times_heap[n] = {}
        times_unsorted_list[n] = {}
        for ratio in ratios:
            logging.info(f"Running {n = } for {ratio = }")
            max_edges = (n * (n - 1)) // 2

            m = int(ratio * max_edges)

            g = create_graph(n, m)

            glb = {"prim_heap": prim_heap,
                   "prim_unsorted_list": prim_unsorted_list, "g": g}

            t1 = timeit.timeit("prim_heap(g)", globals=glb, number=iterations)
            t2 = timeit.timeit("prim_unsorted_list(g)",
                               globals=glb, number=iterations)

            times_heap[n][ratio] = t1
            times_unsorted_list[n][ratio] = t2

    return times_heap, times_unsorted_list


def main() -> None:
    if "--INFO" in sys.argv:
        level = logging.INFO
    elif "--DEBUG" in sys.argv:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    iterations = 100
    for arg in sys.argv:
        if "--iterations=" in arg:
            iterations = int(arg.split("--iterations")[-1])

    logging.basicConfig(level=level)

    ratios = [0.01, 0.05, 0.1, 0.25, 0.35, 0.5, 0.65, 0.75, 0.9, 0.95, 0.99, 1]
    ns = [10, 20, 50, 100, 200, 500, 1000]

    if "--skip-tests" not in sys.argv:
        times_heap, times_unsorted_list = time_functions(
            ratios, ns, iterations=iterations)

        with open("data.json", "w") as f:
            json.dump([times_heap, times_unsorted_list], f)

    else:
        with open("data.json") as f:
            d1, d2 = json.load(f)
            times_heap = {int(k1): {float(k2): v for k2, v in d.items()}
                          for k1, d in d1.items()}
            times_unsorted_list = {
                int(k1): {float(k2): v for k2, v in d.items()} for k1, d in d2.items()}

    # dict_zip is not written by me.
    # It is written by MCoding. Original source code can be found
    # here https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/101_zip_dict/zip_dict.py
    # I do not take any credit for writing dict_zip

    for n, d1, d2 in dict_zip(times_heap, times_unsorted_list):
        logging.info(f"Plotting {n = }")
        ax = plt.subplot()
        ax.set_title(f"{n = }")
        ax.plot(d1.keys(), d1.values(), "r", label="Heap APQ")
        ax.plot(d2.keys(), d2.values(), "b", label="Unsorted List APQ")
        ax.legend()

        path = f"./figures/{n=}"
        plt.savefig(path)
        plt.cla()


if __name__ == "__main__":
    main()
