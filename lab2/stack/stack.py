from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class StackOverflowException(Exception): ...


class StackEmptyException(Exception): ...


class IStack(ABC, Generic[T]):
    @abstractmethod
    def push(self, value: T) -> None: ...

    @abstractmethod
    def peek(self) -> T: ...

    @abstractmethod
    def peek_or_none(self) -> Optional[T]: ...

    @abstractmethod
    def pop(self) -> T: ...

    @abstractmethod
    def pop_or_none(self) -> Optional[T]: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def __bool__(self) -> bool: ...

    @property
    @abstractmethod
    def capacity(self) -> int: ...

    @abstractmethod
    def __len__(self) -> int: ...
