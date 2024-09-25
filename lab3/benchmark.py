from __future__ import annotations

from random import randint, sample
from typing import List

from common import benchmark
from common.benchmark import Benchmark, BenchmarkCallback
from common.extra_typing import override
from lab3.serializers.ordered_binary_tree_serializer import OrderedBinaryTreeSerializer
from lab3.trees.avl_tree import AVLTree
from lab3.trees.ordered_binary_tree import IOrderedBinaryTree
from lab3.trees.ternary_trie import TernaryTrie
from lab3.trees.trie import ITrie


class AVLTreeBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.tree: IOrderedBinaryTree[int] = AVLTree()
        self.n: int = 100000

    def benchmark_insert(self) -> BenchmarkCallback:
        def callback() -> None:
            self.tree.insert(randint(0, self.n))

        return callback, self.n

    def benchmark_delete(self) -> BenchmarkCallback:
        values: List[int] = sample(range(self.n), self.n)
        index: int = 0

        for value in values:
            self.tree.insert(value)

        def callback() -> None:
            nonlocal index
            self.tree.delete(values[index])
            index += 1

        return callback, self.n

    def benchmark_contains(self) -> BenchmarkCallback:
        for i in range(self.n):
            self.tree.insert(i)

        def callback() -> None:
            self.tree.contains(randint(0, self.n))

        return callback, self.n


class AVLTreeStateHydratedBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.tree: IOrderedBinaryTree[int] = AVLTree()
        self.n: int = 100000

    @override
    def tearDown(self) -> None:
        import os

        try:
            os.remove("data.json")
        except FileNotFoundError:
            pass

    def benchmark_file_save(self) -> BenchmarkCallback:
        for i in range(self.n):
            self.tree.insert(randint(0, self.n))

        self.n = 1

        def callback() -> None:
            OrderedBinaryTreeSerializer.save_tree_to_file(self.tree, "data.json")

        return callback, self.n

    def benchmark_file_load(self) -> BenchmarkCallback:
        for i in range(self.n):
            self.tree.insert(randint(0, self.n))

        OrderedBinaryTreeSerializer.save_tree_to_file(self.tree, "data.json")
        self.tree.clear()
        self.n = 1

        def callback() -> None:
            OrderedBinaryTreeSerializer.load_tree_from_file(self.tree, "data.json", int)

        return callback, self.n


class TernaryTrieBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.trie: ITrie[str, int] = TernaryTrie()
        self.n: int = 100000

    def _rand_string(self, n: int) -> str:
        return "".join([chr(randint(97, 122)) for _ in range(n)])

    def benchmark_insert(self) -> BenchmarkCallback:

        def callback() -> None:
            self.trie.put(self._rand_string(10), randint(0, self.n))

        return callback, self.n

    def benchmark_delete(self) -> BenchmarkCallback:
        keys: List[str] = [self._rand_string(10) for _ in range(self.n)]
        index: int = 0

        for key in keys:
            self.trie.put(key, randint(0, self.n))

        def callback() -> None:
            nonlocal index
            self.trie.delete(keys[index])
            index += 1

        return callback, self.n

    def benchmark_contains(self) -> BenchmarkCallback:
        keys: List[str] = [self._rand_string(10) for _ in range(self.n)]

        for key in keys:
            self.trie.put(key, randint(0, self.n))

        def callback() -> None:
            self.trie.contains(keys[randint(0, self.n - 1)])

        return callback, self.n


if __name__ == "__main__":
    benchmark.main()
