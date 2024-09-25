from __future__ import annotations

from typing import TypeVar, Union

from common.comparable import default_compare_to
from lab2.linked_list.doubly_linked_list import DoubleNode, DoublyLinkedList
from lab5.type_aliases import SearchComparator, SearchKeySelector, SearchSequence, T

N = TypeVar("N", bound=Union[int, float])


def interpolation_search(
    sequence: SearchSequence[N],
    target: N,
    compare: SearchComparator[N] = default_compare_to,
) -> int:
    if isinstance(sequence, DoublyLinkedList):
        return _interpolation_search_nodes(sequence, target, lambda x: x, compare)

    return interpolation_search_by(sequence, target, lambda x: x, compare)


def interpolation_search_by(
    sequence: SearchSequence[T],
    target: N,
    key_selector: SearchKeySelector[T, N],
    compare: SearchComparator[N] = default_compare_to,
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
    key_selector: SearchKeySelector[T, N],
    compare: SearchComparator[N] = default_compare_to,
) -> int:
    if sequence._head is None or sequence._tail is None:
        return -1

    low, high = 0, len(sequence) - 1
    head: DoubleNode[T] = sequence._head
    tail: DoubleNode[T] = sequence._tail

    while (
        compare(sequence_low := key_selector(head.value), target) <= 0
        and compare(sequence_high := key_selector(tail.value), target) >= 0
        and compare(sequence_low, sequence_high) != 0
    ):
        ratio: float = (target - sequence_low) / (sequence_high - sequence_low)  # type: ignore[operator]
        position: int = low + int(ratio * (high - low))

        steps_from_head: int = position - low
        steps_from_tail: int = high - position
        node: DoubleNode[T] = head if steps_from_head < steps_from_tail else tail

        if steps_from_head < steps_from_tail:
            while steps_from_head > 0:
                assert node.next is not None
                node = node.next
                steps_from_head -= 1
        else:
            while steps_from_tail > 0:
                assert node.prev is not None
                node = node.prev
                steps_from_tail -= 1

        compare_result: int = compare(key_selector(node.value), target)

        if compare_result == 0:
            return position

        if compare_result < 0:
            low = position + 1
            assert node.next is not None
            head = node.next
        else:
            high = position - 1
            assert node.prev is not None
            tail = node.prev

    if compare(key_selector(head.value), target) == 0:
        return low

    return -1
