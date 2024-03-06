from __future__ import annotations  # for compatibility with older Python versions
import random

from graph import Graph, Edge, Vertex


def create_graph(n: int, m: int) -> Graph:
    g = Graph()

    vertices = [Vertex("0")]

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
        g.add_edge(e)

    for _ in range(m - n + 1):
        # Vertex 0 and Vertex 1 are always connected
        v1, v2 = vertices[0], vertices[1]
        # so the while loop will always run at least once

        while (v1.label, v2.label) not in edges or (v2.label, v1.label) not in edges:
            # Get two vertices that have not been connected already
            v1, v2 = random.choices(vertices, k=2)

        w = random.randint(1, 20)

        e = Edge(v1, v2, w, w)

        edges.add((v1.label, v2.label))
        g.add_edge(e)

    return g


def main() -> None:
    pass


if __name__ == "__main__":
    main()
