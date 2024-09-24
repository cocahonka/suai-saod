from __future__ import annotations

from typing import Callable, List, Optional, Sequence, Tuple, TypeVar, Union

from common.comparable import Comparable, default_compare
from lab2.linked_list.doubly_linked_list import DoubleNode, DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList
from lab4.arrays.array import IArray
from lab4.arrays.dynamic_array import DynamicArray
from lab5.main import Comparator, SearchSequence, T


def interpolation_search(
    sequence: SearchSequence[T],
    target: T,
    compare: Comparator[T] = default_compare,
) -> int:
    raise NotImplemented
