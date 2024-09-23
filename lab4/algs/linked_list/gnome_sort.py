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
    index: int = 1
    while index < len(linked_list):
        if index > 0 and compare(current := linked_list[index], previous := linked_list[index - 1]):
            linked_list[index], linked_list[index - 1] = previous, current
            index -= 1
        else:
            index += 1


def gnome_sort_through_node(
    linked_list: DoublyLinkedList[T],
    compare: Callable[[T, T], bool] = default_compare,
) -> None:
    if linked_list._head is None:
        return

    current_node: Optional[DoubleNode[T]] = linked_list._head.next
    while current_node is not None:
        if current_node.prev is not None and compare(
            current_value := current_node.value,
            previous_value := current_node.prev.value,
        ):
            current_node.value, current_node.prev.value = previous_value, current_value
            current_node = current_node.prev
        else:
            current_node = current_node.next
