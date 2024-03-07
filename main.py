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


def main() -> None:
    random.seed(0)
    g = create_graph(20, 25)
    apq = HeapAPQ()
    tree = prim(g, apq)
    print(tree)
    print(str(tree) == "[Edge(9, Vertex(2), Vertex(0), 9), Edge(14, Vertex(1), Vertex(0), 14), Edge(13, Vertex(18), Vertex(1), 13), Edge(16, Vertex(3), Vertex(2), 16), Edge(10, Vertex(4), Vertex(3), 10), Edge(4, Vertex(12), Vertex(4), 4), Edge(5, Vertex(4), Vertex(16), 5), Edge(5, Vertex(7), Vertex(4), 5), Edge(5, Vertex(8), Vertex(4), 5), Edge(7, Vertex(6), Vertex(4), 7), Edge(12, Vertex(5), Vertex(3), 12), Edge(18, Vertex(17), Vertex(5), 18), Edge(11, Vertex(17), Vertex(13), 11), Edge(3, Vertex(13), Vertex(11), 3), Edge(5, Vertex(11), Vertex(9), 5), Edge(11, Vertex(14), Vertex(13), 11), Edge(1, Vertex(14), Vertex(15), 1), Edge(15, Vertex(19), Vertex(15), 15), Edge(18, Vertex(10), Vertex(4), 18)]")


if __name__ == "__main__":
    main()
