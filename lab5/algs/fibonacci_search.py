from __future__ import annotations

from common.comparable import default_compare_to
from lab2.linked_list.doubly_linked_list import DoubleNode, DoublyLinkedList
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
    if sequence._head is None:
        return -1

    if len(sequence) == 1:
        return 0 if compare(key_selector(sequence._head.value), target) == 0 else -1

    fib, fib_1, fib_2, n = 1, 1, 0, len(sequence)

    while n > fib:
        fib, fib_1, fib_2 = fib + fib_1, fib, fib_1

    offset, old_index = -1, 0
    node: DoubleNode[T] = sequence._head

    while fib > 1:
        index: int = min(offset + fib_2, n - 1)
        steps: int = index - old_index

        # Maybe this block doesn't affect the performance of the algorithm
        # Benchmark don't show any significant difference
        if abs(steps) > index or abs(steps) > n - index:
            assert sequence._tail is not None
            node = sequence._head if steps < 0 else sequence._tail
            steps = index if steps < 0 else index - n + 1

        while steps > 0:
            assert node.next is not None
            node = node.next
            steps -= 1

        while steps < 0:
            assert node.prev is not None
            node = node.prev
            steps += 1

        compare_result = compare(key_selector(node.value), target)

        if compare_result == 0:
            return index

        if compare_result < 0:
            offset = index
            fib, fib_1, fib_2 = fib_1, fib_2, fib_1 - fib_2
        else:
            fib, fib_1, fib_2 = fib_2, fib_1 - fib_2, fib_2 - (fib_1 - fib_2)

        old_index = index

    if (
        offset + 1 < n
        and node.next is not None
        and compare(key_selector(node.next.value), target) == 0
    ):
        return offset + 1

    return -1
