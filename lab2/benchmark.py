from __future__ import annotations

from random import randint, sample
from typing import Any, List

from common import benchmark
from common.benchmark import *
from common.extra_typing import override
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList
from lab2.stack.not_growable_stack import NotGrowableStack
from lab2.stack.stack import IStack
from lab2.stack.stack_linked_list import StackLinkedList


class LinkedListBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.linked_list: ILinkedList[Any] = DoublyLinkedList()
        self.n = 100000

    def benchmark_add_in_head(self) -> BenchmarkCallback:
        return (lambda: self.linked_list.add_in_head(1), self.n)

    def benchmark_add_in_tail(self) -> BenchmarkCallback:
        return (lambda: self.linked_list.add_in_tail(1), self.n)

    def benchmark_remove(self) -> BenchmarkCallback:
        self.n = 10000

        for i in range(self.n):
            self.linked_list.add(i)

        shuffled: List[int] = sample(range(self.n), self.n)
        index: int = 0

        def remove() -> None:
            nonlocal index
            value_to_remove: int = shuffled[index]
            self.linked_list.remove(value_to_remove)
            index += 1

        return (remove, self.n)

    def benchmark_remove_at(self) -> BenchmarkCallback:
        self.n = 10000

        for i in range(self.n):
            self.linked_list.add(i)

        def remove_at() -> None:
            index_to_remove: int = randint(0, len(self.linked_list) - 1)
            self.linked_list.remove_at(index_to_remove)

        return (remove_at, self.n)


class StackBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.stack: IStack[Any] = StackLinkedList()
        self.n = 100000

    def benchmark_push(self) -> BenchmarkCallback:
        return (lambda: self.stack.push(1), self.n)

    def benchmark_pop(self) -> BenchmarkCallback:
        for i in range(self.n):
            self.stack.push(i)

        def pop() -> None:
            self.stack.pop()

        return (pop, self.n)


if __name__ == "__main__":
    benchmark.main()
