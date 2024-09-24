from random import randint, sample
from typing import List

from common import benchmark
from common.benchmark import *
from common.extra_typing import override
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab4.algs.arrays.insertion_sort import insertion_sort
from lab4.algs.arrays.merge_sort import merge_sort, merge_sort_in_place
from lab4.algs.linked_list.counting_sort import counting_sort_through_public_api
from lab4.algs.linked_list.gnome_sort import (
    gnome_sort_through_node,
    gnome_sort_through_public_api,
)
from lab4.arrays.array import IArray
from lab4.arrays.dynamic_array import DynamicArray


class DynamicArrayBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.array: IArray[int] = DynamicArray()
        self.n = 2000

    def benchmark_add(self) -> BenchmarkCallback:
        def callback() -> None:
            self.array.add(1)

        return callback, self.n

    def benchmark_get(self) -> BenchmarkCallback:
        self.array.add_all(sample(range(self.n), self.n))

        def callback() -> None:
            self.array.element_at(randint(0, len(self.array) - 1))

        return callback, self.n

    def benchmark_remove(self) -> BenchmarkCallback:
        random_values: List[int] = sample(range(self.n), self.n)
        self.array.add_all(random_values)
        index: int = 0

        def callback() -> None:
            nonlocal index
            self.array.remove(random_values[index])
            index += 1

        return callback, self.n


class SortingBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.array_n = 1000
        self.linked_list_n = 1000

        self.array: List[int] = sample(range(self.array_n), self.array_n)

        self.linked_list: DoublyLinkedList[int] = DoublyLinkedList()
        [self.linked_list.add(x) for x in sample(range(self.linked_list_n), self.linked_list_n)]

    def benchmark_insertion_sort(self) -> BenchmarkCallback:
        def callback() -> None:
            insertion_sort(self.array)

        return callback, 1, self.array_n

    def benchmark_merge_sort(self) -> BenchmarkCallback:
        def callback() -> None:
            merge_sort(self.array)

        return callback, 1, self.array_n

    def benchmark_merge_sort_in_place(self) -> BenchmarkCallback:
        def callback() -> None:
            merge_sort_in_place(self.array)

        return callback, 1, self.array_n

    def benchmark_counting_sort(self) -> BenchmarkCallback:
        def callback() -> None:
            counting_sort_through_public_api(self.linked_list, lambda x: x)

        return callback, 1, self.linked_list_n

    def benchmark_gnome_sort_through_public_api(self) -> BenchmarkCallback:
        def callback() -> None:
            gnome_sort_through_public_api(self.linked_list)

        return callback, 1, self.linked_list_n

    def benchmark_gnome_sort_through_node(self) -> BenchmarkCallback:
        def callback() -> None:
            gnome_sort_through_node(self.linked_list)

        return callback, 1, self.linked_list_n


if __name__ == "__main__":
    benchmark.main()
