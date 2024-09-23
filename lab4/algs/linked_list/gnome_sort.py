from __future__ import annotations

from typing import Callable, Optional, TypeVar

from common.comparable import Comparable, default_compare
from lab2.linked_list.doubly_linked_list import DoubleNode, DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList

T = TypeVar("T", bound=Comparable)


def gnome_sort_through_public_api(
    linked_list: ILinkedList[T],
    compare: Callable[[T, T], bool] = default_compare,
) -> None:
    if linked_list.is_empty():
        return

    i: int = 1
    while i < len(linked_list):
        first, second = linked_list[i], linked_list[i - 1]
        if not compare(first, second):
            i += 1
        else:
            linked_list.update(i, second)
            linked_list.update(i - 1, first)
            if i > 1:
                i -= 1


def gnome_sort_through_node(
    linked_list: DoublyLinkedList[T],
    compare: Callable[[T, T], bool] = default_compare,
) -> None:
    current_node: Optional[DoubleNode[T]] = linked_list._head
    if current_node is None:
        return

    while current_node is not None:
        if current_node.prev is None:
            current_node = current_node.next
        elif compare(current_node.value, current_node.prev.value):
            current_node.value, current_node.prev.value = (
                current_node.prev.value,
                current_node.value,
            )
            current_node = current_node.prev
        else:
            current_node = current_node.next
