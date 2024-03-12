from src.graph import Vertex, Edge, Graph


def test_vertex():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v3 = Vertex("A")

    assert v1 != v2
    assert v1 == v3


def test_edge():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v3 = Vertex("C")

    e1 = Edge(v1, v2, "AB", 2)
    e2 = Edge(v2, v3, "BC", 2)
    e3 = Edge(v2, v1, "AB", 2)
    e4 = Edge(v1, v2, "AB", 5)

    assert e1 != e2
    assert e3 == e1
    assert e1 == e4

    assert e1.opposite(v1) == v2
    assert e2.opposite(v2) == v3


def test_graph():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v3 = Vertex("C")

    e1 = Edge(v1, v2, "AB", 2)
    e2 = Edge(v2, v3, "BC", 2)
    e3 = Edge(v1, v2, "AB", 5)
    e4 = Edge(v2, v1, "AB", 2)

    g = Graph()

    g.add_vertex(v1)
    g.add_vertex(v2)
    g.add_vertex(v3)

    g.add_edge(v1, v2, e1)
    g.add_edge(v2, v3, e2)
    g.add_edge(v1, v2, e3)
    g.add_edge(v2, v1, e4)

    assert len(g.vertices) == 3

    assert len(g.edges) == 2  # 2 edges as e1 e3 and e4 are the same

    assert g.num_vertices() == 3

    assert g.num_edges() == 2

    assert g.degree(v2) == 2

    assert g.get_edge(v1, v2) == e1

    assert g.get_edges(v2) == [e1, e2]

    g.remove_edge(e2)

    assert g.num_edges() == 1

    g.remove_vertex(v2)

    assert g.num_vertices() == 2

    assert g.num_edges() == 0
