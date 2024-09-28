from __future__ import annotations

from typing import Generic, List, Optional, Tuple, TypeVar, cast

from lab6.graph.adjacency_matrix_graph import AdjacencyMatrixGraph, Vertex
from lab6.graph.graph import Weight

T = TypeVar("T")


class NegativeWeightException(Exception, Generic[T]):
    def __init__(self, vertex: T) -> None:
        super().__init__(f"Negative weight on vertex {vertex}.")


def dijkstra(
    graph: AdjacencyMatrixGraph[T, Weight],
    from_vertex: T,
    to_vertex: T,
) -> Optional[Tuple[List[T], Weight]]:
    from_index: int = graph._get_vertex_index(from_vertex)
    to_index: int = graph._get_vertex_index(to_vertex)

    visited: List[bool] = [False] * graph.vertex_count
    distance: List[Weight] = [cast(Weight, float("inf"))] * graph.vertex_count  # type: ignore[redundant-cast]
    distance[from_index] = 0

    _calculate_distances(graph, visited, distance)

    if distance[to_index] == float("inf"):
        return None

    min_distance: Weight = distance[to_index]
    return (
        _get_shortest_path(graph, (from_index, from_vertex), (to_index, to_vertex), distance),
        min_distance,
    )


def _calculate_distances(
    graph: AdjacencyMatrixGraph[T, Weight],
    visited: List[bool],
    distance: List[Weight],
) -> None:
    while not all(visited):
        current_vertex: Optional[Vertex[T]] = _get_min_distance_vertex(graph, visited, distance)
        if current_vertex is None:
            return

        for index, successor in graph._get_successors(current_vertex):
            if visited[index]:
                continue

            new_distance: Weight = distance[current_vertex[0]] + cast(
                Weight,
                graph._adjacency_matrix[current_vertex[0]][index],
            )

            if new_distance < 0:
                raise NegativeWeightException(successor)

            if new_distance < distance[index]:
                distance[index] = new_distance

        visited[current_vertex[0]] = True


def _get_min_distance_vertex(
    graph: AdjacencyMatrixGraph[T, Weight],
    visited: List[bool],
    distance: List[Weight],
) -> Optional[Vertex[T]]:
    min_distance: float = float("inf")
    min_vertex: Optional[Vertex[T]] = None

    for i in range(graph.vertex_count):
        if visited[i]:
            continue

        if distance[i] < min_distance:
            min_distance = distance[i]
            min_vertex = (i, graph._vertices[i])

    return min_vertex


def _get_shortest_path(
    graph: AdjacencyMatrixGraph[T, Weight],
    from_vertex: Vertex[T],
    to_vertex: Vertex[T],
    distance: List[Weight],
) -> List[T]:
    path: List[T] = []
    current_vertex: Vertex[T] = to_vertex

    while current_vertex != from_vertex:
        min_distance: Weight = distance[current_vertex[0]]
        path.insert(0, current_vertex[1])

        for index, vertex in graph._get_predecessors(current_vertex):
            if distance[index] == float("inf"):
                continue

            is_previous_vertex_exist: bool = (
                distance[index] + cast(Weight, graph._adjacency_matrix[index][current_vertex[0]])
                == min_distance
            )

            if is_previous_vertex_exist:
                distance[current_vertex[0]] = cast(Weight, float("inf"))  # type: ignore[redundant-cast]
                current_vertex = (index, vertex)
                break

    path.insert(0, from_vertex[1])
    return path
