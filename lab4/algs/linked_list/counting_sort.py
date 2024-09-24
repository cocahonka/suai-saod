from typing import Callable, Iterator, List, Tuple, TypeVar

from lab2.linked_list.linked_list import ILinkedList

T = TypeVar("T")


def counting_sort_through_public_api(
    linked_list: ILinkedList[T],
    key_selector: Callable[[T], int],
    ascending: bool = True,
) -> None:
    if not linked_list:
        return

    keys: List[int] = list(map(key_selector, linked_list))

    min_key = max_key = keys[0]
    [(min_key := min(min_key, key), max_key := max(max_key, key)) for key in keys]

    frequency: List[int] = [0] * (max_key - min_key + 1)
    for key in keys:
        frequency[key - min_key] += 1

    positions: List[int] = frequency.copy()
    for i in range(1, len(positions)):
        positions[i] += positions[i - 1]

    sorted_array: List[T] = [element for element in linked_list]
    iterator: Iterator[Tuple[T, int]] = zip(linked_list, keys)
    if not ascending:
        iterator = reversed(list(iterator))

    for element, key in iterator:
        shifted_key = key - min_key
        positions[shifted_key] -= 1
        sorted_array[positions[shifted_key]] = element

    linked_list.clear()
    [linked_list.add(element) for element in sorted_array]
