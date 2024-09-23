from __future__ import annotations

from typing import Callable, TypeVar

from common.comparable import Comparable, default_compare
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
