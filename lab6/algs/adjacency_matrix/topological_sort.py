from __future__ import annotations

from typing import List, TypeVar

from lab6.graph.adjacency_matrix_graph import AdjacencyMatrixGraph, Vertex
from lab6.graph.graph import Weight

T = TypeVar("T")


class CycleInGraphException(Exception):
    def __init__(self) -> None:
        super().__init__("Cycle in graph. Topological sort is not possible.")


class NotDirectedGraphException(Exception):
    def __init__(self) -> None:
        super().__init__("Graph is not directed. Topological sort is not possible.")


def topological_sort(graph: AdjacencyMatrixGraph[T, Weight]) -> List[T]:
    if graph.is_cyclic:
        raise CycleInGraphException()

    if not graph.is_directed:
        raise NotDirectedGraphException()

    visited: List[bool] = [False] * graph.vertex_count
    stack: List[T] = []

    for index, vertex in enumerate(graph._vertices):
        if not visited[index]:
            _topological_sort(graph, stack, visited, (index, vertex))

    return stack


def _topological_sort(
    graph: AdjacencyMatrixGraph[T, Weight],
    stack: List[T],
    visited: List[bool],
    vertex: Vertex[T],
) -> None:
    visited[vertex[0]] = True

    for index, successor in graph._get_successors(vertex):
        if not visited[index]:
            _topological_sort(graph, stack, visited, (index, successor))

    stack.append(vertex[1])
