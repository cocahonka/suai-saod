from __future__ import annotations

from typing import TypeVar, Union

from common.comparable import default_compare_to
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab5.main import Comparator, KeySelector, SearchSequence, T

N = TypeVar("N", bound=Union[int, float])


def interpolation_search(
    sequence: SearchSequence[N],
    target: N,
    compare: Comparator[N] = default_compare_to,
) -> int:
    if isinstance(sequence, DoublyLinkedList):
        return _interpolation_search_nodes(sequence, target, lambda x: x, compare)

    return interpolation_search_by(sequence, target, lambda x: x, compare)


def interpolation_search_by(
    sequence: SearchSequence[T],
    target: N,
    key_selector: KeySelector[T, N],
    compare: Comparator[N] = default_compare_to,
) -> int:
    if not sequence:
        return -1

    low, high = 0, len(sequence) - 1

    while (
        compare(sequence_low := key_selector(sequence[low]), target) <= 0
        and compare(sequence_high := key_selector(sequence[high]), target) >= 0
        and compare(sequence_low, sequence_high) != 0
    ):
        ratio: float = (target - sequence_low) / (sequence_high - sequence_low)  # type: ignore[operator]
        position: int = low + int(ratio * (high - low))

        compare_result: int = compare(key_selector(sequence[position]), target)

        if compare_result == 0:
            return position

        if compare_result < 0:
            low = position + 1
        else:
            high = position - 1

    if compare(key_selector(sequence[low]), target) == 0:
        return low

    return -1


def _interpolation_search_nodes(
    sequence: DoublyLinkedList[T],
    target: N,
    key_selector: KeySelector[T, N],
    compare: Comparator[N] = default_compare_to,
) -> int:
    return interpolation_search_by(sequence, target, key_selector, compare)
