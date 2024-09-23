from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, Sequence, TypeVar, Union, overload

T = TypeVar("T")


class ArrayIndexOutOfBoundsException(Exception): ...


class ArrayOverflowException(Exception): ...


class IArray(ABC, Sequence[T], Generic[T]):
    # Create
    @abstractmethod
    def add(self, value: T) -> None: ...

    @abstractmethod
    def add_all(self, values: Sequence[T]) -> None: ...

    @abstractmethod
    def insert(self, index: int, value: T) -> None: ...

    # Read
    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> IArray[T]: ...

    @abstractmethod
    def __getitem__(self, obj: Union[int, slice]) -> Union[T, IArray[T]]: ...

    @abstractmethod
    def element_at(self, index: int) -> T: ...

    @abstractmethod
    def element_at_or_none(self, index: int) -> Optional[T]: ...

    @abstractmethod
    def index_of(self, value: T) -> int: ...

    @abstractmethod
    def __len__(self) -> int: ...

    def contains(self, value: T) -> bool:
        return value in self

    # Update
    @abstractmethod
    def __setitem__(self, index: int, value: T) -> None: ...

    # Delete
    @abstractmethod
    def remove(self, value: T) -> bool: ...

    @abstractmethod
    def remove_at(self, index: int) -> T: ...

    @abstractmethod
    def clear(self) -> None: ...

    # Utils
    @abstractmethod
    def __str__(self) -> str: ...
