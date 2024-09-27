from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Callable, Generic, Iterator, List, Optional, Tuple, TypeVar

T = TypeVar("T")
Weight = TypeVar("Weight", int, float)


class GraphError(Exception): ...


class VertexNotFoundError(GraphError, Generic[T]):
    def __init__(self, vertex: T) -> None:
        super().__init__(f"Vertex {vertex} not found in the graph.")


class EdgeNotFoundError(GraphError, Generic[T]):
    def __init__(self, from_vertex: T, to_vertex: T) -> None:
        super().__init__(f"Edge from {from_vertex} to {to_vertex} not found in the graph.")


class GraphTraversalType(Enum):
    BREADTH_FIRST = auto()
    DEPTH_FIRST = auto()


class IGraph(ABC, Generic[T, Weight]):
    @property
    @abstractmethod
    def is_directed(self) -> bool: ...

    @property
    @abstractmethod
    def is_cyclic(self) -> bool: ...

    @property
    @abstractmethod
    def is_connected(self) -> bool: ...

    @property
    @abstractmethod
    def edge_count(self) -> int: ...

    @property
    @abstractmethod
    def vertex_count(self) -> int: ...

    @property
    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def __bool__(self) -> bool: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def add(self, vertex: T) -> bool: ...

    @abstractmethod
    def add_all(self, vertices: List[T]) -> None: ...

    @abstractmethod
    def remove(self, vertex: T) -> bool: ...

    @abstractmethod
    def remove_all(self, vertices: List[T]) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def connect(
        self,
        from_vertex: T,
        to_vertex: T,
        weight: Optional[Weight] = None,
    ) -> None: ...

    @abstractmethod
    def disconnect(self, from_vertex: T, to_vertex: T) -> None: ...

    @abstractmethod
    def contains(self, vertex: T) -> bool: ...

    @abstractmethod
    def __contains__(self, vertex: T) -> bool: ...

    @abstractmethod
    def is_connected_to(self, from_vertex: T, to_vertex: T) -> bool: ...

    @abstractmethod
    def get_weight(self, from_vertex: T, to_vertex: T) -> Optional[Weight]: ...

    @abstractmethod
    def get_predecessors(self, to_vertex: T) -> List[T]: ...

    @abstractmethod
    def get_successors(self, from_vertex: T) -> List[T]: ...

    @abstractmethod
    def get_neighbors(self, vertex: T) -> List[T]: ...

    @abstractmethod
    def get_edges(self) -> List[Tuple[T, T, Optional[Weight]]]: ...

    @abstractmethod
    def get_path(self, from_vertex: T, to_vertex: T) -> List[T]: ...

    @abstractmethod
    def get_all_paths(self, from_vertex: T, to_vertex: T) -> List[List[T]]: ...

    @abstractmethod
    def traverse(
        self,
        action: Callable[[T], None],
        traverse_type: GraphTraversalType = GraphTraversalType.DEPTH_FIRST,
        start_vertex: Optional[T] = None,
    ) -> None: ...

    @abstractmethod
    def generator(
        self,
        traverse_type: GraphTraversalType = GraphTraversalType.DEPTH_FIRST,
        start_vertex: Optional[T] = None,
    ) -> Iterator[T]: ...

    @abstractmethod
    def copy(self) -> IGraph[T, Weight]: ...

    @abstractmethod
    def __str__(self) -> str: ...
