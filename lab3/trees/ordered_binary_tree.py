from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Generic, Iterator, Optional, TypeVar

from common.comparable import Comparable

T = TypeVar("T", bound=Comparable)


class OrderedBinaryTreeEmptyException(Exception): ...


class TraversalType(Enum):
    PRE_ORDER = auto()
    IN_ORDER = auto()
    POST_ORDER = auto()


@dataclass
class BinaryNode(Generic[T]):
    value: T
    left: Optional[BinaryNode[T]] = None
    right: Optional[BinaryNode[T]] = None


class IOrderedBinaryTree(ABC, Generic[T]):
    @property
    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def insert(self, value: T) -> None: ...

    @abstractmethod
    def contains(self, value: T) -> bool: ...

    @abstractmethod
    def find_max(self) -> T: ...

    @abstractmethod
    def find_min(self) -> T: ...

    @abstractmethod
    def delete(self, value: T) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def traverse(
        self,
        action: Callable[[T], None],
        traverse_type: TraversalType = TraversalType.IN_ORDER,
    ) -> None: ...

    @abstractmethod
    def generator(self, traverse_type: TraversalType = TraversalType.IN_ORDER) -> Iterator[T]: ...

    @abstractmethod
    def __str__(self) -> str: ...

    def is_empty(self) -> bool:
        return self.size <= 0

    def __contains__(self, value: T) -> bool:
        return self.contains(value)

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return not self.is_empty()
