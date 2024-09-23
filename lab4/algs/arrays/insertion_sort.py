from __future__ import annotations

from typing import Callable, MutableSequence, TypeVar, Union

from common.comparable import Comparable, default_compare
from lab4.arrays.array import IArray

T = TypeVar("T", bound=Comparable)


def insertion_sort(
    array: Union[IArray[T], MutableSequence[T]],
    compare: Callable[[T, T], bool] = default_compare,
) -> None:
    for i in range(1, len(array)):
        value: T = array[i]
        j: int = i - 1
        while j >= 0 and compare(value, array[j]):
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = value
