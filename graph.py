class DoesNotExistError(Exception):
    pass


class Vertex:
    def __init__(self, label: str = "") -> None:
        self.label = label

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.label})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.label)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Vertex):
            raise TypeError
        return self.label == __value.label


class Edge:
    def __init__(self, vertex_1: Vertex, vertex_2: Vertex, label: str, weight: int) -> None:
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
        self.label = label
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.label}, {self.vertex_1}, {self.vertex_2}, {self.weight})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash((self.vertex_1, self.vertex_2, self.label))

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Edge):
            raise TypeError
        return (self.vertex_1, self.vertex_2, self.label) == (__value.vertex_1, __value.vertex_2, __value.label)


class Graph:
    def __init__(self,):
        self.vertices: dict[Vertex, dict[Vertex, Edge]] = {}
        self.edges: dict[Edge, tuple[Vertex, Vertex]] = {}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(vertices=[{', '.join(str(v) for v in self.vertices.keys())}], edges=[{', '.join(str(e) for e in self.edges.keys())}])"

    def __repr__(self) -> str:
        return str(self)

    def num_vertices(self) -> int:
        return len(self.vertices)

    def num_edges(self) -> int:
        return len(self.edges)

    def add_vertex(self, x: Vertex) -> None:
        self.vertices[x] = {}

    def add_edge(self, x: Vertex, y: Vertex, e: Edge) -> None:
        self.vertices[x][y] = e
        self.vertices[y][x] = e
        self.edges[e] = (x, y)

    def degree(self, x: Vertex) -> int:
        return len(self.vertices[x].keys())

    def get_edge(self, x: Vertex, y: Vertex) -> Edge:
        e = self.vertices[x].get(y, None) if e in self.edges else None
        if e is None:
            raise DoesNotExistError
        return e

    def get_edges(self, x: Vertex) -> list[Edge]:
        return list(self.vertices[x].values())

    def remove_edge(self, e: Edge) -> None:
        if e not in self.edges:
            raise DoesNotExistError
        del self.edges[e]
        del self.vertices[e.vertex_1][e.vertex_2]
        del self.vertices[e.vertex_2][e.vertex_1]

    def remove_vertex(self, x: Vertex) -> None:
        if x not in self.vertices:
            raise DoesNotExistError
        for edge in self.vertices[x].values():
            del self.edges[edge]
        del self.vertices[x]
