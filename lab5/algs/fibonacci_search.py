from __future__ import annotations

from common.comparable import default_compare_to
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab5.main import C, Comparator, KeySelector, SearchSequence, T


def fibonacci_search(
    sequence: SearchSequence[C],
    target: C,
    compare: Comparator[C] = default_compare_to,
) -> int:
    if isinstance(sequence, DoublyLinkedList):
        return _fibonacci_search_nodes(sequence, target, lambda x: x, compare)

    return fibonacci_search_by(sequence, target, lambda x: x, compare)


def fibonacci_search_by(
    sequence: SearchSequence[T],
    target: C,
    key_selector: KeySelector[T, C],
    compare: Comparator[C] = default_compare_to,
) -> int:
    fib, fib_1, fib_2, n = 1, 1, 0, len(sequence)

    while n > fib:
        fib, fib_1, fib_2 = fib + fib_1, fib, fib_1

    offset: int = -1

    while fib > 1:
        index: int = min(offset + fib_2, n - 1)

        compare_result = compare(key_selector(sequence[index]), target)

        if compare_result == 0:
            return index

        if compare_result < 0:
            offset = index
            fib, fib_1, fib_2 = fib_1, fib_2, fib_1 - fib_2
        else:
            fib, fib_1, fib_2 = fib_2, fib_1 - fib_2, fib_2 - (fib_1 - fib_2)

    if offset + 1 < n and compare(key_selector(sequence[offset + 1]), target) == 0:
        return offset + 1

    return -1


def _fibonacci_search_nodes(
    sequence: DoublyLinkedList[T],
    target: C,
    key_selector: KeySelector[T, C],
    compare: Comparator[C] = default_compare_to,
) -> int:
    return fibonacci_search_by(sequence, target, key_selector, compare)
