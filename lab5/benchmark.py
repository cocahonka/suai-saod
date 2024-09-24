from random import randint
from typing import List

from common import benchmark
from common.benchmark import *
from common.extra_typing import override
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab4.arrays.dynamic_array import DynamicArray
from lab5.algs.fibonacci_search import fibonacci_search
from lab5.algs.interpolation_search import interpolation_search


class SearchBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.list_n: int = 10000
        self.array_n: int = 10000
        self.linked_list_n: int = 10000

        self.lower_bound: int = -1000
        self.upper_bound: int = 1000

        self.list: List[int] = [
            randint(self.lower_bound, self.upper_bound) for _ in range(self.list_n)
        ]
        self.array: DynamicArray[int] = DynamicArray()
        self.array.add_all(self.list)
        self.linked_list: DoublyLinkedList[int] = DoublyLinkedList()
        [self.linked_list.add(x) for x in self.list]

    def benchmark_fibonacci_search_list(self) -> BenchmarkCallback:
        def callback() -> None:
            fibonacci_search(self.list, randint(self.lower_bound, self.upper_bound))

        return callback, self.list_n

    def benchmark_fibonacci_search_array(self) -> BenchmarkCallback:
        def callback() -> None:
            fibonacci_search(self.array, randint(self.lower_bound, self.upper_bound))

        return callback, self.array_n

    def benchmark_fibonacci_search_linked_list(self) -> BenchmarkCallback:
        def callback() -> None:
            fibonacci_search(self.linked_list, randint(self.lower_bound, self.upper_bound))

        return callback, self.linked_list_n

    def benchmark_interpolation_search_list(self) -> BenchmarkCallback:
        def callback() -> None:
            interpolation_search(self.list, randint(self.lower_bound, self.upper_bound))

        return callback, self.list_n

    def benchmark_interpolation_search_array(self) -> BenchmarkCallback:
        def callback() -> None:
            interpolation_search(self.array, randint(self.lower_bound, self.upper_bound))

        return callback, self.array_n

    def benchmark_interpolation_search_linked_list(self) -> BenchmarkCallback:
        def callback() -> None:
            interpolation_search(self.linked_list, randint(self.lower_bound, self.upper_bound))

        return callback, self.linked_list_n


if __name__ == "__main__":
    benchmark.main()
