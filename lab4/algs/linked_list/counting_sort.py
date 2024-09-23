from typing import Callable, TypeVar

from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList

T = TypeVar("T")


def counting_sort_through_public_api(
    linked_list: ILinkedList[T],
    key: Callable[[T], int],
) -> None:
    if linked_list.is_empty():
        return

    min_key = key(linked_list.element_at(0))
    max_key = key(linked_list.element_at(0))

    for i in range(1, len(linked_list)):
        k = key(linked_list.element_at(i))
        if k < min_key:
            min_key = k
        if k > max_key:
            max_key = k

    count = [0] * (max_key - min_key + 1)

    for i in range(len(linked_list)):
        count[key(linked_list.element_at(i)) - min_key] += 1

    sorted_elements = []
    for i in range(len(count)):
        while count[i] > 0:
            for j in range(len(linked_list)):
                if key(linked_list.element_at(j)) == i + min_key:
                    sorted_elements.append(linked_list.element_at(j))
                    break
            count[i] -= 1

    for i, value in enumerate(sorted_elements):
        linked_list.update(i, value)


if __name__ == "__main__":
    linked_list: ILinkedList[int] = DoublyLinkedList()
    [linked_list.add(x) for x in [-3, -1, 4, 2, 0]]
    counting_sort_through_public_api(linked_list, lambda x: x)
    print([x for x in linked_list])
