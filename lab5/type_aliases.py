from __future__ import annotations

from typing import Callable, Sequence, TypeVar, Union

from common.comparable import Comparable
from lab2.linked_list.linked_list import ILinkedList

C = TypeVar("C", bound=Comparable)
T = TypeVar("T")
SearchSequence = Union[Sequence[T], ILinkedList[T]]
SearchKeySelector = Callable[[T], C]
SearchComparator = Callable[[C, C], int]
SearchFunction = Callable[
    [
        SearchSequence[C],
        C,
        SearchComparator[C],
    ],
    int,
]
SearchByFunction = Callable[
    [
        SearchSequence[T],
        C,
        SearchKeySelector[T, C],
        SearchComparator[C],
    ],
    int,
]
