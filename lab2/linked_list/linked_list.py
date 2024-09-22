from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


class ILinkedList(ABC, Generic[T]):
    # Create
    @abstractmethod
    def add(self, value: T) -> None: ...

    @abstractmethod
    def add_in_head(self, value: T) -> None: ...

    @abstractmethod
    def add_in_tail(self, value: T) -> None: ...

    @abstractmethod
    def insert(self, index: int, value: T) -> None: ...

    # Read
    @abstractmethod
    def element_at(self, index: int) -> T: ...

    @abstractmethod
    def element_at_or_none(self, index: int) -> Optional[T]: ...

    @abstractmethod
    def __getitem__(self, index: int) -> T: ...

    @abstractmethod
    def contains(self, value: T) -> bool: ...

    @abstractmethod
    def __contains__(self, value: T) -> bool: ...

    # Update
    @abstractmethod
    def update(self, index: int, value: T) -> None: ...

    @abstractmethod
    def __setitem__(self, index: int, value: T) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    # Delete
    @abstractmethod
    def remove(self, value: T) -> bool: ...

    @abstractmethod
    def remove_at(self, index: int) -> None: ...

    @abstractmethod
    def __delitem__(self, index: int) -> None: ...

    # Utility
    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def __bool__(self) -> bool: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __str__(self) -> str: ...

    # Iteration
    @abstractmethod
    def __iter__(self) -> Iterator[T]: ...

    @abstractmethod
    def __next__(self) -> T: ...

    @abstractmethod
    def __reversed__(self) -> Iterator[T]: ...

    @abstractmethod
    def reverse(self) -> None: ...
