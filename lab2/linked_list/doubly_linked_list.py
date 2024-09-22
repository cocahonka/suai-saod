from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Final, Generic, Iterator, Optional

from common.extra_typing import override
from lab2.linked_list.linked_list import ILinkedList, T


@dataclass
class DoubleNode(Generic[T]):
    value: T
    next: Optional[DoubleNode[T]] = None
    prev: Optional[DoubleNode[T]] = None


class DoublyLinkedList(ILinkedList[T], Generic[T]):
    def __init__(self) -> None:
        self._head: Optional[DoubleNode[T]] = None
        self._tail: Optional[DoubleNode[T]] = None
        self._current: Optional[DoubleNode[T]] = None
        self._length: int = 0

    # Create
    @override
    def add(self, value: T) -> None:
        self.add_in_tail(value)

    @override
    def add_in_head(self, value: T) -> None:
        node: Final[DoubleNode[T]] = DoubleNode(value)
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._length += 1

    @override
    def add_in_tail(self, value: T) -> None:
        node: Final[DoubleNode[T]] = DoubleNode(value)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._length += 1

    @override
    def insert(self, index: int, value: T) -> None:
        if index == 0:
            self.add_in_head(value)
        elif index == self._length:
            self.add_in_tail(value)
        else:
            current: Final[DoubleNode[T]] = self._efficient_get_node_by_index(index)
            node: Final[DoubleNode[T]] = DoubleNode(value)
            node.prev = current.prev
            node.next = current
            assert current.prev is not None
            current.prev.next = node
            current.prev = node
            self._length += 1

    # Read
    def _efficient_get_node_by_index(self, index: int) -> DoubleNode[T]:
        if index < 0 or index >= self._length:
            raise IndexError("Index out of range")

        current: Optional[DoubleNode[T]] = None
        if index < self._length // 2:
            current = self._head
            for _ in range(index):
                assert current is not None
                current = current.next
        else:
            current = self._tail
            for _ in range(self._length - 1, index, -1):
                assert current is not None
                current = current.prev

        assert current is not None
        return current

    def _get_node_by_predicate(
        self, test: Callable[[DoubleNode[T]], bool]
    ) -> Optional[DoubleNode[T]]:
        current: Optional[DoubleNode[T]] = self._head
        while current is not None:
            if test(current):
                return current
            current = current.next
        return None

    @override
    def element_at(self, index: int) -> T:
        return self._efficient_get_node_by_index(index).value

    @override
    def element_at_or_none(self, index: int) -> Optional[T]:
        try:
            return self.element_at(index)
        except IndexError:
            return None

    @override
    def __getitem__(self, index: int) -> T:
        return self.element_at(index)

    @override
    def contains(self, value: T) -> bool:
        for element in self:
            if element == value:
                return True
        return False

    @override
    def __contains__(self, value: T) -> bool:
        return self.contains(value)

    # Update
    @override
    def update(self, index: int, value: T) -> None:
        self._efficient_get_node_by_index(index).value = value

    @override
    def __setitem__(self, index: int, value: T) -> None:
        self.update(index, value)

    @override
    def clear(self) -> None:
        self._head = None
        self._tail = None
        self._current = None
        self._length = 0

    # Delete
    @override
    def remove(self, value: T) -> bool:
        current: Optional[DoubleNode[T]] = self._get_node_by_predicate(
            lambda node: node.value == value
        )
        if current is None:
            return False

        if current.prev is not None:
            current.prev.next = current.next
        else:
            self._head = current.next
        if current.next is not None:
            current.next.prev = current.prev
        else:
            self._tail = current.prev

        self._length -= 1
        return True

    @override
    def remove_at(self, index: int) -> None:
        current: Final[DoubleNode[T]] = self._efficient_get_node_by_index(index)
        if current.prev is not None:
            current.prev.next = current.next
        else:
            self._head = current.next
        if current.next is not None:
            current.next.prev = current.prev
        else:
            self._tail = current.prev
        self._length -= 1

    @override
    def __delitem__(self, index: int) -> None:
        return self.remove_at(index)

    # Utility
    @override
    def is_empty(self) -> bool:
        return self._length == 0

    @override
    def __bool__(self) -> bool:
        return not self.is_empty()

    @override
    def __len__(self) -> int:
        return self._length

    @override
    def __str__(self) -> str:
        return "[" + " -> ".join(str(value) for value in self) + "]"

    # Iteration
    @override
    def __iter__(self) -> Iterator[T]:
        self._current = self._head
        return self

    @override
    def __next__(self) -> T:
        if self._current is None:
            raise StopIteration
        value: Final[T] = self._current.value
        self._current = self._current.next
        return value

    @override
    def __reversed__(self) -> Iterator[T]:
        current: Optional[DoubleNode[T]] = self._tail

        while current is not None:
            yield current.value
            current = current.prev

    @override
    def reverse(self) -> None:
        current: Optional[DoubleNode[T]] = self._head
        self._head, self._tail = self._tail, self._head
        while current is not None:
            current.next, current.prev = current.prev, current.next
            current = current.prev
