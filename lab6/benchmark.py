from random import randint, sample
from typing import List

from common import benchmark
from common.benchmark import Benchmark, BenchmarkCallback
from common.extra_typing import override
from lab6.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from lab6.graph.graph import GraphTraversalType


class GraphBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.graph: AdjacencyMatrixGraph[int, int] = AdjacencyMatrixGraph(is_directed=True)

        self.n: int = 2500

    def benchmark_add_vertex(self) -> BenchmarkCallback:
        values: List[int] = sample(range(self.n), self.n)
        index: int = 0

        def callback() -> None:
            nonlocal index
            self.graph.add(values[index])
            index += 1

        return callback, self.n

    def benchmark_remove_vertex(self) -> BenchmarkCallback:
        values: List[int] = sample(range(self.n), self.n)
        index: int = 0

        self.graph.add_all(sample(range(self.n), self.n))

        def callback() -> None:
            nonlocal index
            self.graph.remove(values[index])
            index += 1

        return callback, self.n

    def benchmark_traverse_dfs(self) -> BenchmarkCallback:
        values: List[int] = sample(range(self.n), self.n)

        self.graph.add_all(values)

        def callback() -> None:
            self.graph.traverse(lambda _: None, GraphTraversalType.DEPTH_FIRST)

        return callback, 5, self.n

    def benchmark_traverse_bfs(self) -> BenchmarkCallback:
        values: List[int] = sample(range(self.n), self.n)

        self.graph.add_all(values)

        def callback() -> None:
            self.graph.traverse(lambda _: None, GraphTraversalType.BREADTH_FIRST)

        return callback, 5, self.n

    def benchmark_get_path(self) -> BenchmarkCallback:
        values: List[int] = sample(range(self.n), self.n)

        self.graph.add_all(values)

        def callback() -> None:
            self.graph.get_path(randint(0, self.n - 1), randint(0, self.n - 1))

        return callback, self.n

    def benchmark_get_all_paths(self) -> BenchmarkCallback:
        values: List[int] = sample(range(self.n), self.n)

        self.graph.add_all(values)

        def callback() -> None:
            self.graph.get_all_paths(randint(0, self.n - 1), randint(0, self.n - 1))

        return callback, self.n


class GraphHydratedBenchmark(Benchmark): ...


class GraphAlgsBenchmark(Benchmark): ...


if __name__ == "__main__":
    benchmark.main()
