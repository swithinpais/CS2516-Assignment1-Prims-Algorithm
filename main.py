from __future__ import annotations  # for compatibility with older Python versions

import random
import math

from graph import Graph, Edge, Vertex
from priority_queue import APQ, HeapAPQ, UnsortedListAPQ, Element


def create_graph(n: int, m: int) -> Graph:
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
            v1, v2 = random.choices(vertices, k=2)

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


def main() -> None:
    pass


if __name__ == "__main__":
    main()
