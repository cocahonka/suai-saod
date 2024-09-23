from __future__ import annotations

import ctypes
from abc import ABC, abstractmethod
from typing import Any, Final, Iterator, Optional, Sequence, Union, cast, overload

from common.extra_typing import override
from lab4.arrays.array import ArrayIndexOutOfBoundsException, IArray, T

_CArray = ctypes.Array[Any]


class ResizeStrategy(ABC):
    @abstractmethod
    def is_needed(
        self,
        current_capacity: int,
        current_size: int,
    ) -> bool: ...

    @abstractmethod
    def calculate_capacity(
        self,
        current_capacity: int,
        current_size: int,
    ) -> int: ...


class DoubleResizeStrategy(ResizeStrategy):
    @override
    def is_needed(
        self,
        current_capacity: int,
        current_size: int,
    ) -> bool:
        return current_size == current_capacity

    @override
    def calculate_capacity(
        self,
        current_capacity: int,
        current_size: int,
    ) -> int:
        return 2 * current_capacity


class DynamicArray(IArray[T]):
    def __init__(
        self,
        initial_capacity: int = 10,
        resize_strategy: ResizeStrategy = DoubleResizeStrategy(),
    ) -> None:
        if initial_capacity < 0:
            raise ValueError("Initial capacity must be greater than or equal to 0")

        self._size: int = 0
        self._capacity: int = initial_capacity
        self._initial_capacity: int = initial_capacity
        self._resize_strategy: ResizeStrategy = resize_strategy
        self._array: _CArray = self._make_array(self._capacity)

    def _make_array(self, capacity: int) -> _CArray:
        return (capacity * ctypes.py_object)()

    def _resize(self) -> None:
        new_capacity: Final[int] = self._resize_strategy.calculate_capacity(
            self._capacity,
            self._size,
        )
        assert new_capacity > self._capacity

        new_array: Final[_CArray] = self._make_array(new_capacity)
        for i in range(self._size):
            new_array[i] = self._array[i]

        self._array = new_array
        self._capacity = new_capacity

    @override
    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._array[i]

    @override
    def add(self, value: T) -> None:
        if self._resize_strategy.is_needed(self._capacity, self._size):
            self._resize()

        self._array[self._size] = value
        self._size += 1

    @override
    def add_all(self, values: Sequence[T]) -> None:
        for value in values:
            self.add(value)

    @override
    def insert(self, index: int, value: T) -> None:
        if index < 0 or index >= self._size:
            raise ArrayIndexOutOfBoundsException(
                f"Index {index} out of bounds ({0}..{self._size - 1})"
            )

        if self._resize_strategy.is_needed(self._capacity, self._size):
            self._resize()

        for i in range(self._size, index, -1):
            self._array[i] = cast(T, self._array[i - 1])

        self._array[index] = value
        self._size += 1

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> DynamicArray[T]: ...

    @override
    def __getitem__(self, obj: Union[int, slice]) -> Union[T, DynamicArray[T]]:
        if isinstance(obj, int):
            if obj < 0:
                obj += len(self)
            if obj < 0 or obj >= len(self):
                raise ArrayIndexOutOfBoundsException(
                    f"Index {obj} out of bounds ({0}..{self._size - 1})"
                )
            return cast(T, self._array[obj])

        if isinstance(obj, slice):
            result: Final[DynamicArray[T]] = DynamicArray(self._capacity)
            result.add_all([self[i] for i in range(*obj.indices(len(self)))])
            return result

        raise TypeError(f"Invalid argument type: {type(obj).__name__}")

    @override
    def element_at(self, index: int) -> T:
        return self[index]

    @override
    def element_at_or_none(self, index: int) -> Optional[T]:
        return self[index] if 0 <= index < self._size else None

    @override
    def index_of(self, value: T) -> int:
        for i in range(self._size):
            if self._array[i] == value:
                return i
        return -1

    @override
    def __len__(self) -> int:
        return self._size

    @override
    def update(self, index: int, value: T) -> None:
        if index < 0 or index >= self._size:
            raise ArrayIndexOutOfBoundsException(
                f"Index {index} out of bounds ({0}..{self._size - 1})"
            )
        self._array[index] = value

    @override
    def remove(self, value: T) -> bool:
        index: int = self.index_of(value)
        if index != -1:
            self.remove_at(index)
            return True
        return False

    @override
    def remove_at(self, index: int) -> T:
        if index < 0 or index >= self._size:
            raise ArrayIndexOutOfBoundsException(
                f"Index {index} out of bounds ({0}..{self._size - 1})"
            )

        value: Final[T] = cast(T, self._array[index])
        for i in range(index, self._size - 1):
            self._array[i] = cast(T, self._array[i + 1])
        self._size -= 1
        return value

    @override
    def clear(self) -> None:
        self._size = 0
        self._capacity = self._initial_capacity
        self._array = self._make_array(self._capacity)

    @override
    def __str__(self) -> str:
        return f"DynamicArray({self._array[:self._size]})"
