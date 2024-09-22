from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import (
    Callable,
    Generic,
    Iterator,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    overload,
)

from common.comparable import Comparable
from common.extra_typing import Self

K = TypeVar("K", bound="TrieKey")
V = TypeVar("V")


class TrieElementNotFound(Exception): ...


class TrieKey(Protocol):
    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, object: int) -> Comparable: ...

    @overload
    def __getitem__(self, slice: slice) -> Self: ...


class TraverseType(Enum):
    PRE_ORDER = auto()
    IN_ORDER = auto()
    POST_ORDER = auto()


class ITrie(ABC, Generic[K, V]):
    @property
    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def put(self, key: K, value: V) -> None: ...

    @abstractmethod
    def get_or_none(self, key: K) -> Optional[V]: ...

    def get(self, key: K) -> V:
        value: Optional[V] = self.get_or_none(key)
        if value is None:
            raise TrieElementNotFound(f"Key {key} not found")
        return value

    def __getitem__(self, key: K) -> V:
        return self.get(key)

    def contains(self, key: K) -> bool:
        return self.get_or_none(key) is not None

    @abstractmethod
    def keys_with_prefix(self, prefix: K) -> Iterator[K]: ...

    @abstractmethod
    def longest_prefix_of(self, query: K) -> Optional[K]: ...

    def merge(self, other: ITrie[K, V]) -> None:
        for key, value in other.generator(TraverseType.IN_ORDER):
            self.put(key, value)

    @abstractmethod
    def delete(self, key: K) -> bool: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def traverse(
        self,
        action: Callable[[K, V], None],
        traverse_type: TraverseType = TraverseType.IN_ORDER,
    ) -> None: ...

    @abstractmethod
    def generator(
        self, traverse_type: TraverseType = TraverseType.IN_ORDER
    ) -> Iterator[Tuple[K, V]]: ...

    @abstractmethod
    def __str__(self) -> str: ...

    def is_empty(self) -> bool:
        return self.size <= 0

    def __contains__(self, key: K) -> bool:
        return self.contains(key)

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return not self.is_empty()
