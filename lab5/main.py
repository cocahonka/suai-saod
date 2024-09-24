from __future__ import annotations

from typing import Callable, Sequence, TypeVar, Union

from common.comparable import Comparable
from lab2.linked_list.linked_list import ILinkedList

T = TypeVar("T", bound=Comparable)
Comparator = Callable[[T, T], bool]
SearchSequence = Union[Sequence[T], ILinkedList[T]]
SearchFunction = Callable[[SearchSequence[T], T, Comparator[T]], int]


def main() -> None: ...


if __name__ == "__main__":
    main()
