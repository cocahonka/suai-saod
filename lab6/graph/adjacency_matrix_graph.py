from __future__ import annotations

from typing import Callable, Iterator, List, Optional, Set, Tuple, TypeVar, cast

from common.extra_typing import override
from lab6.graph.graph import (
    GraphTraversalType,
    IGraph,
    SelfConnectionError,
    VertexNotFoundError,
    Weight,
)

T = TypeVar("T")
Vertex = Tuple[int, T]


class AdjacencyMatrixGraph(IGraph[T, Weight]):
    def __init__(self, is_directed: bool = False) -> None:
        self._is_directed: bool = is_directed
        self._adjacency_matrix: List[List[Optional[Weight]]] = []
        self._vertices: List[T] = []

    def _get_vertex_index(self, vertex: T) -> int:
        try:
            return self._vertices.index(vertex)
        except ValueError as e:
            raise VertexNotFoundError(vertex) from e

    def _vzip(self, vertex: T) -> Vertex[T]:
        return self._get_vertex_index(vertex), vertex

    @property
    @override
    def is_directed(self) -> bool:
        return self._is_directed

    @property
    @override
    def is_cyclic(self) -> bool:
        black: List[bool] = [False] * len(self._vertices)
        gray: List[bool] = [False] * len(self._vertices)

        for index, vertex in enumerate(self._vertices):
            if not black[index]:
                if self._is_cyclic(index, (index, vertex), black, gray):
                    return True

        return False

    def _is_cyclic(
        self,
        from_index: int,
        vertex: Vertex[T],
        black: List[bool],
        gray: List[bool],
    ) -> bool:
        vertex_index: int = vertex[0]
        black[vertex_index] = True
        gray[vertex_index] = True

        for index, successor in self._get_successors(vertex):
            if not self._is_directed and index == from_index:
                continue

            if not black[index]:
                if self._is_cyclic(vertex_index, (index, successor), black, gray):
                    return True
            elif gray[index]:
                return True

        gray[vertex_index] = False

        return False

    @property
    @override
    def is_connected(self) -> bool:
        if not self._vertices:
            return True

        visited: List[bool] = [False] * len(self._vertices)

        self._is_connected((0, self._vertices[0]), visited)

        return all(visited)

    def _is_connected(self, vertex: Vertex[T], visited: List[bool]) -> None:
        visited[vertex[0]] = True

        for index, neighbor in self._get_neighbors(vertex):
            if not visited[index]:
                self._is_connected((index, neighbor), visited)

    @property
    @override
    def edge_count(self) -> int:
        return sum(
            1 for line in self._adjacency_matrix for weight in line if weight is not None
        ) // (1 + int(not self._is_directed))

    @property
    @override
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    @override
    def is_empty(self) -> bool:
        return not self._vertices

    @override
    def __bool__(self) -> bool:
        return not self.is_empty

    @override
    def __len__(self) -> int:
        return len(self._vertices)

    @override
    def add(self, vertex: T) -> bool:
        if vertex in self._vertices:
            return False

        self._vertices.append(vertex)
        for row in self._adjacency_matrix:
            row.append(None)
        self._adjacency_matrix.append([None] * len(self._vertices))

        return True

    @override
    def add_all(self, vertices: List[T]) -> None:
        for vertex in vertices:
            self.add(vertex)

    @override
    def remove(self, vertex: T) -> bool:
        if vertex not in self._vertices:
            return False

        index = self._vertices.index(vertex)
        self._vertices.pop(index)
        for row in self._adjacency_matrix:
            row.pop(index)
        self._adjacency_matrix.pop(index)

        return True

    @override
    def remove_all(self, vertices: List[T]) -> None:
        for vertex in vertices:
            self.remove(vertex)

    @override
    def clear(self) -> None:
        self._vertices.clear()
        self._adjacency_matrix.clear()

    @override
    def connect(
        self,
        from_vertex: T,
        to_vertex: T,
        weight: Weight = 0,
    ) -> None:
        from_index: int = self._get_vertex_index(from_vertex)
        to_index: int = self._get_vertex_index(to_vertex)

        if from_index == to_index:
            raise SelfConnectionError(from_vertex)

        self._adjacency_matrix[from_index][to_index] = weight
        if not self._is_directed:
            self._adjacency_matrix[to_index][from_index] = weight

    @override
    def connect_all(self, edges: List[Tuple[T, T, Weight]]) -> None:
        for from_vertex, to_vertex, weight in edges:
            self.connect(from_vertex, to_vertex, weight)

    @override
    def disconnect(self, from_vertex: T, to_vertex: T) -> None:
        self.connect(from_vertex, to_vertex, None)  # type: ignore[arg-type]

    @override
    def disconnect_all(self, edges: List[Tuple[T, T]]) -> None:
        for from_vertex, to_vertex in edges:
            self.disconnect(from_vertex, to_vertex)

    @override
    def contains(self, vertex: T) -> bool:
        return vertex in self._vertices

    @override
    def __contains__(self, vertex: T) -> bool:
        return self.contains(vertex)

    @override
    def is_connected_to(
        self,
        from_vertex: T,
        to_vertex: T,
        bidirectional: bool = False,
    ) -> bool:
        from_index: int = self._get_vertex_index(from_vertex)
        to_index: int = self._get_vertex_index(to_vertex)

        is_from_connected: bool = self._adjacency_matrix[from_index][to_index] is not None

        if not bidirectional:
            return is_from_connected

        is_to_connected: bool = self._adjacency_matrix[to_index][from_index] is not None

        return is_from_connected and is_to_connected

    @override
    def get_weight(self, from_vertex: T, to_vertex: T) -> Weight:
        from_index: int = self._get_vertex_index(from_vertex)
        to_index: int = self._get_vertex_index(to_vertex)

        return cast(Weight, self._adjacency_matrix[from_index][to_index])

    @override
    def get_predecessors(self, to_vertex: T) -> List[T]:
        return [vertex for _, vertex in self._get_predecessors(self._vzip(to_vertex))]

    def _get_predecessors(self, to_vertex: Vertex[T]) -> List[Vertex[T]]:
        return [
            (i, self._vertices[i])
            for i, line in enumerate(self._adjacency_matrix)
            if line[to_vertex[0]] is not None
        ]

    @override
    def get_successors(self, from_vertex: T) -> List[T]:
        return [vertex for _, vertex in self._get_successors(self._vzip(from_vertex))]

    def _get_successors(self, from_vertex: Vertex[T]) -> List[Vertex[T]]:
        return [
            (i, self._vertices[i])
            for i, weight in enumerate(self._adjacency_matrix[from_vertex[0]])
            if weight is not None
        ]

    @override
    def get_neighbors(self, vertex: T) -> List[T]:
        return [neighbor for _, neighbor in self._get_neighbors(self._vzip(vertex))]

    def _get_neighbors(self, vertex: Vertex[T]) -> List[Vertex[T]]:
        if self._is_directed:
            return self._get_predecessors(vertex) + self._get_successors(vertex)

        return self._get_successors(vertex)

    @override
    def get_edges(self) -> List[Tuple[T, T, Optional[Weight]]]:
        edges: List[Tuple[T, T, Optional[Weight]]] = []

        for from_index, line in enumerate(self._adjacency_matrix):
            for to_index, weight in enumerate(line):
                if weight is not None:
                    edges.append((self._vertices[from_index], self._vertices[to_index], weight))

        return edges

    @override
    def get_path(self, from_vertex: T, to_vertex: T) -> List[T]:
        visited: List[bool] = [False] * len(self._vertices)
        path: List[T] = []

        self._get_path(self._vzip(from_vertex), self._vzip(to_vertex), visited, path)

        return path

    def _get_path(
        self,
        from_vertex: Vertex[T],
        to_vertex: Vertex[T],
        visited: List[bool],
        path: List[T],
    ) -> bool:
        if from_vertex == to_vertex:
            path.insert(0, from_vertex[1])
            return True

        visited[from_vertex[0]] = True

        for index, successor in self._get_successors(from_vertex):
            if not visited[index] and self._get_path((index, successor), to_vertex, visited, path):
                path.insert(0, from_vertex[1])
                return True

        return False

    @override
    def get_all_paths(self, from_vertex: T, to_vertex: T) -> List[List[T]]:
        visited: List[bool] = [False] * len(self._vertices)
        paths: List[List[T]] = []
        current_path: List[T] = []

        self._get_all_paths(
            self._vzip(from_vertex),
            self._vzip(to_vertex),
            visited,
            paths,
            current_path,
        )

        return paths

    def _get_all_paths(
        self,
        from_vertex: Vertex[T],
        to_vertex: Vertex[T],
        visited: List[bool],
        paths: List[List[T]],
        current_path: List[T],
    ) -> None:
        current_path.append(from_vertex[1])

        if from_vertex == to_vertex:
            paths.append(list(current_path))
        else:
            visited[from_vertex[0]] = True

            for index, successor in self._get_successors(from_vertex):
                if not visited[index]:
                    self._get_all_paths(
                        (index, successor),
                        to_vertex,
                        visited,
                        paths,
                        current_path,
                    )

            visited[from_vertex[0]] = False

        current_path.pop()

    @override
    def traverse(
        self,
        action: Callable[[T], None],
        traverse_type: GraphTraversalType = GraphTraversalType.DEPTH_FIRST,
        start_vertex: Optional[T] = None,
    ) -> None:
        match traverse_type:
            case GraphTraversalType.DEPTH_FIRST:
                method = self._dfs
            case GraphTraversalType.BREADTH_FIRST:
                method = self._bfs

        visited: List[bool] = [False] * len(self._vertices)

        if start_vertex is not None:
            method(self._vzip(start_vertex), visited, action)

        for index, vertex in enumerate(self._vertices):
            if not visited[index]:
                method((index, vertex), visited, action)

    def _dfs(
        self,
        vertex: Vertex[T],
        visited: List[bool],
        action: Callable[[T], None],
    ) -> None:
        visited[vertex[0]] = True
        action(vertex[1])

        for index, successor in self._get_successors(vertex):
            if not visited[index]:
                self._dfs((index, successor), visited, action)

    def _bfs(
        self,
        vertex: Vertex[T],
        visited: List[bool],
        action: Callable[[T], None],
    ) -> None:
        visited[vertex[0]] = True
        queue: List[Vertex[T]] = [vertex]

        while queue:
            vertex = queue.pop(0)
            action(vertex[1])

            for index, successor in self._get_successors(vertex):
                if not visited[index]:
                    visited[index] = True
                    queue.append((index, successor))

    @override
    def generator(
        self,
        traverse_type: GraphTraversalType = GraphTraversalType.DEPTH_FIRST,
        start_vertex: Optional[T] = None,
    ) -> Iterator[T]:
        match traverse_type:
            case GraphTraversalType.DEPTH_FIRST:
                method = self._dfs_generator
            case GraphTraversalType.BREADTH_FIRST:
                method = self._bfs_generator

        visited: List[bool] = [False] * len(self._vertices)

        if start_vertex is not None:
            yield from method(self._vzip(start_vertex), visited)

        for index, vertex in enumerate(self._vertices):
            if not visited[index]:
                yield from method((index, vertex), visited)

    def _dfs_generator(self, vertex: Vertex[T], visited: List[bool]) -> Iterator[T]:
        visited[vertex[0]] = True
        yield vertex[1]

        for index, successor in self._get_successors(vertex):
            if not visited[index]:
                yield from self._dfs_generator((index, successor), visited)

    def _bfs_generator(self, vertex: Vertex[T], visited: List[bool]) -> Iterator[T]:
        visited[vertex[0]] = True
        queue: List[Vertex[T]] = [vertex]

        while queue:
            vertex = queue.pop(0)
            yield vertex[1]

            for index, successor in self._get_successors(vertex):
                if not visited[index]:
                    visited[index] = True
                    queue.append((index, successor))

    @override
    def copy(self) -> AdjacencyMatrixGraph[T, Weight]:
        graph: AdjacencyMatrixGraph[T, Weight] = AdjacencyMatrixGraph(self._is_directed)
        graph._vertices = self._vertices.copy()
        graph._adjacency_matrix = [row.copy() for row in self._adjacency_matrix]

        return graph

    @override
    def __str__(self) -> str:
        if self.is_empty:
            return f"{self.__class__.__name__} is empty"

        str_vertices: List[str] = list(map(str, self._vertices))
        max_length_weight: int = max(
            len(str(weight))
            for line in self._adjacency_matrix
            for weight in line
            if weight is not None
        )

        matrix_header: List[str] = [
            f"{'':<{max_length_weight}} | {' | '.join(str(vertex)[:max_length_weight].center(max_length_weight) for vertex in str_vertices)} |"
        ]

        str_matrix: List[str] = matrix_header + [
            f"{vertex[:max_length_weight]:<{max_length_weight}} | {' | '.join(str(weight).center(max_length_weight) if weight is not None else '-' * max_length_weight for weight in line)} |"
            for vertex, line in zip(str_vertices, self._adjacency_matrix)
        ]

        return f"{self.__class__.__name__}:\n" + "\n".join(str_matrix)
