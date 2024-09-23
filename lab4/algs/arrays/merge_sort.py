from __future__ import annotations

from typing import Callable, MutableSequence, TypeVar, Union

from common.comparable import Comparable, default_compare
from lab4.arrays.array import IArray

T = TypeVar("T", bound=Comparable)


def merge_sort_in_place(
    array: Union[IArray[T], MutableSequence[T]],
    compare: Callable[[T, T], bool] = default_compare,
) -> None:
    buffer: Union[IArray[T], MutableSequence[T]] = array[::]

    def _merge_sort(left: int, right: int) -> None:
        if left >= right:
            return

        middle: int = (left + right) // 2
        _merge_sort(left, middle)
        _merge_sort(middle + 1, right)

        i: int = left
        j: int = middle + 1
        k: int = left

        while i <= middle or j <= right:
            if j > right or (i <= middle and compare(array[i], array[j])):
                buffer[k] = array[i]
                i += 1
            else:
                buffer[k] = array[j]
                j += 1
            k += 1

        for i in range(left, right + 1):
            array[i] = buffer[i]

    _merge_sort(0, len(array) - 1)


def merge_sort(
    array: Union[IArray[T], MutableSequence[T]],
    compare: Callable[[T, T], bool] = default_compare,
) -> None:
    if len(array) <= 1:
        return

    middle: int = len(array) // 2
    left: Union[IArray[T], MutableSequence[T]] = array[:middle]
    right: Union[IArray[T], MutableSequence[T]] = array[middle:]

    merge_sort(left, compare)
    merge_sort(right, compare)

    i: int = 0
    j: int = 0
    k: int = 0

    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            array[k] = left[i]
            i += 1
        else:
            array[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        array[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        array[k] = right[j]
        j += 1
        k += 1
