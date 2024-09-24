from typing import Protocol

from common.extra_typing import Self


class Comparable(Protocol):
    def __lt__(self, other: Self) -> bool: ...
    def __le__(self, other: Self) -> bool: ...
    def __gt__(self, other: Self) -> bool: ...
    def __ge__(self, other: Self) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...


def default_compare(a: Comparable, b: Comparable) -> bool:
    return a < b


def default_compare_to(a: Comparable, b: Comparable) -> int:
    if a < b:
        return -1
    if a > b:
        return 1
    return 0
