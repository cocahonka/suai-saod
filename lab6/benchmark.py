from random import randint, sample
from typing import List

from common import benchmark
from common.benchmark import Benchmark, BenchmarkCallback
from common.extra_typing import override
from lab6.algs.adjacency_matrix.dijkstra import dijkstra
from lab6.algs.adjacency_matrix.topological_sort import topological_sort
from lab6.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from lab6.graph.graph import GraphTraversalType
from lab6.serializers.graph_serializer import GraphSerializer


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


class GraphHydratedBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.graph: AdjacencyMatrixGraph[int, int] = AdjacencyMatrixGraph(is_directed=True)
        self.filename: str = "data.json"
        self.n: int = 5000

    @override
    def tearDown(self) -> None:
        import os

        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def benchmark_file_save(self) -> BenchmarkCallback:
        self.graph.add_all(sample(range(self.n), self.n))

        def callback() -> None:
            GraphSerializer.save_graph_to_file(self.graph, self.filename)

        return callback, 1, self.n

    def benchmark_file_load(self) -> BenchmarkCallback:
        self.graph.add_all(sample(range(self.n), self.n))

        GraphSerializer.save_graph_to_file(self.graph, self.filename)
        self.graph.clear()

        def callback() -> None:
            GraphSerializer.load_graph_from_file(self.graph, self.filename, int)

        return callback, 1, self.n


class GraphAlgsBenchmark(Benchmark):
    @override
    def setUp(self) -> None:
        self.n: int = 2500

    def benchmark_directed_dijkstra(self) -> BenchmarkCallback:
        directed_graph: AdjacencyMatrixGraph[int, int] = AdjacencyMatrixGraph(is_directed=True)
        directed_graph.add_all(sample(range(self.n), self.n))

        def callback() -> None:
            dijkstra(directed_graph, randint(0, self.n - 1), randint(0, self.n - 1))

        return callback, self.n

    def benchmark_undirected_dijkstra(self) -> BenchmarkCallback:
        undirected_graph: AdjacencyMatrixGraph[int, int] = AdjacencyMatrixGraph(is_directed=False)
        undirected_graph.add_all(sample(range(self.n), self.n))

        def callback() -> None:
            dijkstra(undirected_graph, randint(0, self.n - 1), randint(0, self.n - 1))

        return callback, self.n

    def benchmark_topological_sort(self) -> BenchmarkCallback:
        elements_count: int = 100
        directed_graphs: List[AdjacencyMatrixGraph[int, int]] = [
            AdjacencyMatrixGraph(is_directed=True) for _ in range(self.n)
        ]

        for directed_graph in directed_graphs:
            directed_graph.add_all(sample(range(elements_count), elements_count))

        index: int = 0

        def callback() -> None:
            nonlocal index
            topological_sort(directed_graphs[index])
            index += 1

        return callback, self.n, elements_count


if __name__ == "__main__":
    benchmark.main()
