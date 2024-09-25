from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Generic, Optional

from common.extra_typing import override
from lab2.stack.stack import IStack, StackEmptyException, T


@dataclass
class SingleNode(Generic[T]):
    value: T
    next: Optional[SingleNode[T]] = None


class StackLinkedList(IStack[T]):
    def __init__(self) -> None:
        self._head: Optional[SingleNode[T]] = None
        self._length: int = 0

    @override
    def push(self, value: T) -> None:
        node: SingleNode[T] = SingleNode(value)
        if self._head is None:
            self._head = node
        else:
            node.next = self._head
            self._head = node
        self._length += 1

    @override
    def peek(self) -> T:
        if self._head is None:
            raise StackEmptyException("Stack is empty")
        return self._head.value

    @override
    def peek_or_none(self) -> Optional[T]:
        return self._head.value if self._head is not None else None

    @override
    def pop(self) -> T:
        value: Final[Optional[T]] = self.pop_or_none()
        if value is None:
            raise StackEmptyException("Stack is empty")
        return value

    @override
    def pop_or_none(self) -> Optional[T]:
        if self._head is None:
            return None
        value: T = self._head.value
        self._head = self._head.next
        self._length -= 1
        return value

    @override
    def clear(self) -> None:
        self._head = None
        self._length = 0

    @override
    @property
    def capacity(self) -> int:
        return self._length

    @override
    def is_empty(self) -> bool:
        return self._length <= 0

    @override
    def __bool__(self) -> bool:
        return not self.is_empty()

    @override
    def __len__(self) -> int:
        return self._length
