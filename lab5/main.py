from __future__ import annotations

from typing import Callable, Sequence, TypeVar, Union

from common.comparable import Comparable
from lab2.linked_list.linked_list import ILinkedList

C = TypeVar("C", bound=Comparable)
T = TypeVar("T")
SearchSequence = Union[Sequence[T], ILinkedList[T]]
KeySelector = Callable[[T], C]
Comparator = Callable[[C, C], int]
SearchFunction = Callable[
    [
        SearchSequence[C],
        C,
        Comparator[C],
    ],
    int,
]
SearchByFunction = Callable[
    [
        SearchSequence[T],
        C,
        KeySelector[T, C],
        Comparator[C],
    ],
    int,
]


def main() -> None: ...


if __name__ == "__main__":
    main()
