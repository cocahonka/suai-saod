from __future__ import annotations

from typing import Final, Iterator, Optional, Sequence, Union, overload

from common.extra_typing import override
from lab4.arrays.array import ArrayOverflowException, IArray, T


class NotGrowableArray(IArray[T]):
    def __init__(self, delegate: IArray[T], capacity: int):
        self._delegate: Final[IArray[T]] = delegate
        self._capacity: Final[int] = capacity

    def _is_full(self) -> bool:
        return len(self._delegate) == self._capacity

    @override
    def add(self, value: T) -> None:
        if self._is_full():
            raise ArrayOverflowException("Array is full")
        return self._delegate.add(value)

    @override
    def add_all(self, values: Sequence[T]) -> None:
        if len(self._delegate) + len(values) > self._capacity:
            raise ArrayOverflowException("Array is full")
        return self._delegate.add_all(values)

    @override
    def insert(self, index: int, value: T) -> None:
        if self._is_full():
            raise ArrayOverflowException("Array is full")
        return self._delegate.insert(index, value)

    @overload
    @override
    def __getitem__(self, index: int) -> T: ...

    @overload
    @override
    def __getitem__(self, index: slice) -> IArray[T]: ...

    @override
    def __getitem__(self, obj: Union[int, slice]) -> Union[T, IArray[T]]:
        return self._delegate[obj]

    @override
    def element_at(self, index: int) -> T:
        return self._delegate.element_at(index)

    @override
    def element_at_or_none(self, index: int) -> Optional[T]:
        return self._delegate.element_at_or_none(index)

    @override
    def index_of(self, value: T) -> int:
        return self._delegate.index_of(value)

    @override
    def __len__(self) -> int:
        return len(self._delegate)

    @override
    def contains(self, value: T) -> bool:
        return self._delegate.contains(value)

    @override
    def update(self, index: int, value: T) -> None:
        return self._delegate.update(index, value)

    @override
    def remove(self, value: T) -> bool:
        return self._delegate.remove(value)

    @override
    def remove_at(self, index: int) -> T:
        return self._delegate.remove_at(index)

    @override
    def clear(self) -> None:
        return self._delegate.clear()

    @override
    def __str__(self) -> str:
        return self._delegate.__str__()

    @override
    def __iter__(self) -> Iterator[T]:
        return iter(self._delegate)
