from __future__ import annotations

from typing import Callable, TypeVar

from common.comparable import Comparable, default_compare
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
