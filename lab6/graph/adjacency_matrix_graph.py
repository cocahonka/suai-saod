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


# TODO: Rethink _get_vertex_index, get_successors, get_predecessors, get_neighbors methods
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
                if self._is_cyclic(vertex, black, gray):
                    return True

        return False

    def _is_cyclic(self, vertex: T, black: List[bool], gray: List[bool]) -> bool:
        black[self._get_vertex_index(vertex)] = True
        gray[self._get_vertex_index(vertex)] = True

        for successor in self.get_successors(vertex):
            successor_index: int = self._get_vertex_index(successor)
            if not black[successor_index]:
                if self._is_cyclic(successor, black, gray):
                    return True
            elif gray[successor_index]:
                return True

        gray[self._get_vertex_index(vertex)] = False

        return False

    @property
    @override
    def is_connected(self) -> bool:
        if not self._vertices:
            return True

        visited: List[bool] = [False] * len(self._vertices)

        self._is_connected(self._vertices[0], visited)

        return all(visited)

    def _is_connected(self, vertex: T, visited: List[bool]) -> None:
        visited[self._get_vertex_index(vertex)] = True

        for neighbor in self.get_neighbors(vertex):
            if not visited[self._get_vertex_index(neighbor)]:
                self._is_connected(neighbor, visited)

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
        to_index: int = self._get_vertex_index(to_vertex)

        return [
            self._vertices[i]
            for i, line in enumerate(self._adjacency_matrix)
            if line[to_index] is not None
        ]

    @override
    def get_successors(self, from_vertex: T) -> List[T]:
        from_index: int = self._get_vertex_index(from_vertex)

        return [
            self._vertices[i]
            for i, weight in enumerate(self._adjacency_matrix[from_index])
            if weight is not None
        ]

    @override
    def get_neighbors(self, vertex: T) -> List[T]:
        seen: Set[T] = set()
        neighbors: List[T] = self.get_predecessors(vertex) + self.get_successors(vertex)
        return [x for x in neighbors if x not in seen and not seen.add(x)]  # type: ignore[func-returns-value]
        return list(self.get_predecessors(vertex) + self.get_successors(vertex))

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
        raise NotImplementedError

    @override
    def get_all_paths(self, from_vertex: T, to_vertex: T) -> List[List[T]]:
        raise NotImplementedError

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
            method(start_vertex, visited, action)

        for index, vertex in enumerate(self._vertices):
            if not visited[index]:
                method(vertex, visited, action)

    def _dfs(
        self,
        vertex: T,
        visited: List[bool],
        action: Callable[[T], None],
    ) -> None:
        visited[self._get_vertex_index(vertex)] = True
        action(vertex)

        for successor in self.get_successors(vertex):
            if not visited[self._get_vertex_index(successor)]:
                self._dfs(successor, visited, action)

    def _bfs(
        self,
        vertex: T,
        visited: List[bool],
        action: Callable[[T], None],
    ) -> None:
        visited[self._get_vertex_index(vertex)] = True
        queue: List[T] = [vertex]

        while queue:
            vertex = queue.pop(0)
            action(vertex)

            for successor in self.get_successors(vertex):
                successor_index: int = self._get_vertex_index(successor)
                if not visited[successor_index]:
                    visited[successor_index] = True
                    queue.append(successor)

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
            yield from method(start_vertex, visited)

        for index, vertex in enumerate(self._vertices):
            if not visited[index]:
                yield from method(vertex, visited)

    def _dfs_generator(self, vertex: T, visited: List[bool]) -> Iterator[T]:
        visited[self._get_vertex_index(vertex)] = True
        yield vertex

        for successor in self.get_successors(vertex):
            if not visited[self._get_vertex_index(successor)]:
                yield from self._dfs_generator(successor, visited)

    def _bfs_generator(self, vertex: T, visited: List[bool]) -> Iterator[T]:
        visited[self._get_vertex_index(vertex)] = True
        queue: List[T] = [vertex]

        while queue:
            vertex = queue.pop(0)
            yield vertex

            for successor in self.get_successors(vertex):
                successor_index: int = self._get_vertex_index(successor)
                if not visited[successor_index]:
                    visited[successor_index] = True
                    queue.append(successor)

    @override
    def copy(self) -> AdjacencyMatrixGraph[T, Weight]:
        graph: AdjacencyMatrixGraph[T, Weight] = AdjacencyMatrixGraph(self._is_directed)
        graph._vertices = self._vertices.copy()
        graph._adjacency_matrix = [row.copy() for row in self._adjacency_matrix]

        return graph

    @override
    def __str__(self) -> str:
        vertices_str: str = ", ".join(map(str, self._vertices))
        matrix_str: str = "\n".join(
            [
                " ".join(["-" if weight is None else str(weight) for weight in line])
                for line in self._adjacency_matrix
            ]
        )

        return f"Vertices: {vertices_str}\nAdjacency Matrix:\n{matrix_str}"
