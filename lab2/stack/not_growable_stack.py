from __future__ import annotations

from typing import Final, Optional

from common.extra_typing import override
from lab2.stack.stack import IStack, StackOverflowException, T


class NotGrowableStack(IStack[T]):
    def __init__(self, delegate: IStack[T], capacity: int):
        self._delegate: Final[IStack[T]] = delegate
        self._capacity: Final[int] = capacity

    def _is_full(self) -> bool:
        return len(self._delegate) == self.capacity

    @override
    def push(self, value: T) -> None:
        if self._is_full():
            raise StackOverflowException("Stack is full")
        return self._delegate.push(value)

    @override
    def peek(self) -> T:
        return self._delegate.peek()

    @override
    def peek_or_none(self) -> Optional[T]:
        return self._delegate.peek_or_none()

    @override
    def pop(self) -> T:
        return self._delegate.pop()

    @override
    def pop_or_none(self) -> Optional[T]:
        return self._delegate.pop_or_none()

    @override
    def clear(self) -> None:
        return self._delegate.clear()

    @override
    @property
    def capacity(self) -> int:
        return self._capacity

    @override
    def is_empty(self) -> bool:
        return self._delegate.is_empty()

    @override
    def __bool__(self) -> bool:
        return bool(self._delegate)

    @override
    def __len__(self) -> int:
        return len(self._delegate)
