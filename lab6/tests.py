from __future__ import annotations

import unittest
from dataclasses import dataclass
from functools import total_ordering
from typing import List

from common.extra_typing import override
from lab6.algs.adjacency_matrix.dijkstra import NegativeWeightException, dijkstra
from lab6.algs.adjacency_matrix.topological_sort import (
    CycleInGraphException,
    NotDirectedGraphException,
    topological_sort,
)
from lab6.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from lab6.graph.graph import (
    GraphTraversalType,
    IGraph,
    SelfConnectionError,
    VertexNotFoundError,
)
from lab6.serializers.graph_serializer import GraphSerializer


class GraphTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.directed_graph = self._create_directed_graph()
        self.undirected_graph = self._create_undirected_graph()

    def _create_directed_graph(self) -> IGraph[str, int]:
        graph = AdjacencyMatrixGraph[str, int](is_directed=True)
        return graph

    def _create_undirected_graph(self) -> IGraph[str, int]:
        graph = AdjacencyMatrixGraph[str, int](is_directed=False)
        return graph

    def test_add(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            self.assertTrue(graph.add("A"))
            self.assertTrue(graph.add("B"))
            self.assertFalse(graph.add("B"))
            self.assertEqual(graph.vertex_count, 2)
            self.assertListEqual([*graph.generator()], ["A", "B"])

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_add_all(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C"])
            self.assertEqual(graph.vertex_count, 3)
            self.assertListEqual([*graph.generator()], ["A", "B", "C"])

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_vertex_count(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            self.assertEqual(graph.vertex_count, 0)
            graph.add_all(["A", "B", "C"])
            self.assertEqual(graph.vertex_count, 3)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_edges_count(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.assertEqual(self.directed_graph.edge_count, 0)
        self.directed_graph.connect("A", "B")
        self.assertEqual(self.directed_graph.edge_count, 1)
        self.directed_graph.connect("B", "C")
        self.assertEqual(self.directed_graph.edge_count, 2)
        self.directed_graph.connect("B", "A")
        self.assertEqual(self.directed_graph.edge_count, 3)

        self.undirected_graph.add_all(["A", "B", "C"])
        self.assertEqual(self.undirected_graph.edge_count, 0)
        self.undirected_graph.connect("A", "B")
        self.assertEqual(self.undirected_graph.edge_count, 1)
        self.undirected_graph.connect("B", "C")
        self.assertEqual(self.undirected_graph.edge_count, 2)
        self.undirected_graph.connect("B", "A")
        self.assertEqual(self.undirected_graph.edge_count, 2)

    def test_is_empty(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            self.assertTrue(graph.is_empty)
            graph.add("A")
            self.assertFalse(graph.is_empty)
            graph.add("B")
            graph.connect("A", "B")
            graph.remove_all(["A", "B"])
            self.assertTrue(graph.is_empty)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_bool_dunder(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            self.assertFalse(bool(graph))
            graph.add("A")
            self.assertTrue(bool(graph))
            graph.add("B")
            graph.connect("A", "B")
            graph.remove_all(["A", "B"])
            self.assertFalse(bool(graph))

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_len_dunder(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            self.assertEqual(len(graph), 0)
            graph.add("A")
            self.assertEqual(len(graph), 1)
            graph.add("B")
            self.assertEqual(len(graph), 2)
            graph.connect("A", "B")
            self.assertEqual(len(graph), 2)
            graph.remove_all(["A", "B"])
            self.assertEqual(len(graph), 0)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_remove(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add("A")
            graph.add("B")
            graph.connect("A", "B")
            self.assertEqual(graph.edge_count, 1)
            self.assertTrue(graph.remove("A"))
            self.assertEqual(graph.edge_count, 0)
            self.assertEqual(graph.vertex_count, 1)
            self.assertFalse(graph.remove("A"))
            self.assertEqual(graph.vertex_count, 1)
            self.assertTrue(graph.remove("B"))
            self.assertEqual(graph.vertex_count, 0)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_remove_all(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C"])
            graph.connect_all(
                [
                    ("A", "B", 0),
                    ("B", "C", 0),
                    ("C", "A", 0),
                ]
            )
            graph.remove_all(["A", "B"])
            self.assertEqual(graph.vertex_count, 1)
            self.assertEqual(graph.edge_count, 0)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_clear(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C"])
            graph.connect_all(
                [
                    ("A", "B", 0),
                    ("B", "C", 0),
                    ("C", "A", 0),
                ]
            )
            graph.clear()
            self.assertEqual(graph.vertex_count, 0)
            self.assertEqual(graph.edge_count, 0)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_connect(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C", 1)
        self.directed_graph.connect("C", "A", -1)
        self.assertRaises(VertexNotFoundError, self.directed_graph.connect, "D", "C")
        self.assertRaises(SelfConnectionError, self.directed_graph.connect, "A", "A")
        self.assertEqual(self.directed_graph.edge_count, 3)
        self.assertListEqual(
            self.directed_graph.get_edges(),
            [
                ("A", "B", 0),
                ("B", "C", 1),
                ("C", "A", -1),
            ],
        )

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C", 1)
        self.undirected_graph.connect("C", "A", -1)
        self.assertRaises(VertexNotFoundError, self.undirected_graph.connect, "D", "C")
        self.assertRaises(SelfConnectionError, self.undirected_graph.connect, "A", "A")
        self.assertEqual(self.undirected_graph.edge_count, 3)
        self.assertListEqual(
            self.undirected_graph.get_edges(),
            [
                ("A", "B", 0),
                ("A", "C", -1),
                ("B", "A", 0),
                ("B", "C", 1),
                ("C", "A", -1),
                ("C", "B", 1),
            ],
        )

    def test_connect_all(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect_all(
            [
                ("A", "B", 1),
                ("B", "C", 2),
                ("C", "A", 3),
            ]
        )
        self.assertRaises(VertexNotFoundError, self.directed_graph.connect_all, [("D", "C", 1)])
        self.assertEqual(self.directed_graph.edge_count, 3)
        self.assertListEqual(
            self.directed_graph.get_edges(),
            [
                ("A", "B", 1),
                ("B", "C", 2),
                ("C", "A", 3),
            ],
        )

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect_all(
            [
                ("A", "B", 1),
                ("B", "C", 2),
                ("C", "A", 3),
            ]
        )
        self.assertRaises(VertexNotFoundError, self.undirected_graph.connect_all, [("D", "C", 1)])
        self.assertEqual(self.undirected_graph.edge_count, 3)
        self.assertListEqual(
            self.undirected_graph.get_edges(),
            [
                ("A", "B", 1),
                ("A", "C", 3),
                ("B", "A", 1),
                ("B", "C", 2),
                ("C", "A", 3),
                ("C", "B", 2),
            ],
        )

    def test_disconnect(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C")
        self.directed_graph.connect("C", "A")
        self.directed_graph.disconnect("A", "B")
        self.assertRaises(VertexNotFoundError, self.directed_graph.disconnect, "D", "C")

        self.assertEqual(self.directed_graph.edge_count, 2)
        self.assertListEqual(
            self.directed_graph.get_edges(),
            [
                ("B", "C", 0),
                ("C", "A", 0),
            ],
        )

        self.directed_graph.disconnect("B", "C")
        self.assertEqual(self.directed_graph.edge_count, 1)
        self.directed_graph.disconnect("C", "A")
        self.assertEqual(self.directed_graph.edge_count, 0)

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C")
        self.undirected_graph.connect("C", "A")
        self.undirected_graph.disconnect("A", "B")
        self.assertRaises(VertexNotFoundError, self.undirected_graph.disconnect, "D", "C")

        self.assertEqual(self.undirected_graph.edge_count, 2)
        self.assertListEqual(
            self.undirected_graph.get_edges(),
            [
                ("A", "C", 0),
                ("B", "C", 0),
                ("C", "A", 0),
                ("C", "B", 0),
            ],
        )

        self.undirected_graph.disconnect("B", "C")
        self.assertEqual(self.undirected_graph.edge_count, 1)
        self.undirected_graph.disconnect("C", "A")
        self.assertEqual(self.undirected_graph.edge_count, 0)

    def test_disconnect_all(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C")
        self.directed_graph.connect("C", "A")
        self.directed_graph.disconnect_all(
            [
                ("A", "B"),
                ("B", "C"),
                ("C", "A"),
            ]
        )
        self.assertEqual(self.directed_graph.edge_count, 0)

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C")
        self.undirected_graph.connect("C", "A")
        self.undirected_graph.disconnect_all(
            [
                ("A", "B"),
                ("B", "C"),
                ("C", "A"),
            ]
        )
        self.assertEqual(self.undirected_graph.edge_count, 0)

    def test_contains(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C"])
            self.assertTrue(graph.contains("A"))
            self.assertTrue(graph.contains("B"))
            self.assertTrue(graph.contains("C"))
            self.assertFalse(graph.contains("D"))

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_contains_dunder(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C"])
            self.assertTrue("A" in graph)
            self.assertTrue("B" in graph)
            self.assertTrue("C" in graph)
            self.assertFalse("D" in graph)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_get_weight(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B", 1)
        self.directed_graph.connect("B", "C", 2)
        self.directed_graph.connect("C", "A", 3)

        self.assertEqual(self.directed_graph.get_weight("A", "B"), 1)
        self.assertIsNone(self.directed_graph.get_weight("A", "C"))
        self.assertEqual(self.directed_graph.get_weight("B", "C"), 2)
        self.assertEqual(self.directed_graph.get_weight("C", "A"), 3)
        self.assertRaises(VertexNotFoundError, self.directed_graph.get_weight, "D", "C")

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B", 1)
        self.undirected_graph.connect("B", "C", 2)
        self.undirected_graph.connect("C", "A", 3)

        self.assertEqual(self.undirected_graph.get_weight("A", "B"), 1)
        self.assertEqual(self.undirected_graph.get_weight("B", "A"), 1)
        self.assertEqual(self.undirected_graph.get_weight("B", "C"), 2)
        self.assertEqual(self.undirected_graph.get_weight("C", "A"), 3)
        self.assertRaises(VertexNotFoundError, self.undirected_graph.get_weight, "D", "C")

    def test_is_connected_to(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C")
        self.directed_graph.connect("C", "A")
        self.directed_graph.connect("A", "C")

        self.assertTrue(self.directed_graph.is_connected_to("A", "B"))
        self.assertFalse(self.directed_graph.is_connected_to("A", "B", bidirectional=True))

        self.assertTrue(self.directed_graph.is_connected_to("B", "C"))
        self.assertTrue(self.directed_graph.is_connected_to("C", "A"))
        self.assertTrue(self.directed_graph.is_connected_to("A", "C"))

        self.assertTrue(self.directed_graph.is_connected_to("A", "C", bidirectional=True))
        self.assertTrue(self.directed_graph.is_connected_to("C", "A", bidirectional=True))

        self.assertFalse(self.directed_graph.is_connected_to("B", "A"))
        self.assertRaises(VertexNotFoundError, self.directed_graph.is_connected_to, "D", "C")

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C")
        self.undirected_graph.connect("C", "A")

        self.assertTrue(self.undirected_graph.is_connected_to("A", "B"))
        self.assertTrue(self.undirected_graph.is_connected_to("B", "C"))
        self.assertTrue(self.undirected_graph.is_connected_to("C", "A"))

        self.assertTrue(self.undirected_graph.is_connected_to("B", "A"))
        self.assertTrue(self.undirected_graph.is_connected_to("C", "B"))
        self.assertTrue(self.undirected_graph.is_connected_to("A", "C"))

        self.assertTrue(self.undirected_graph.is_connected_to("A", "B", bidirectional=True))
        self.assertTrue(self.undirected_graph.is_connected_to("B", "C", bidirectional=True))
        self.assertTrue(self.undirected_graph.is_connected_to("C", "A", bidirectional=True))
        self.assertRaises(VertexNotFoundError, self.undirected_graph.is_connected_to, "D", "C")

    def test_copy(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C", 1)
        self.directed_graph.connect("C", "A", -1)

        copied_graph = self.directed_graph.copy()
        self.assertEqual(copied_graph.vertex_count, 3)
        self.assertEqual(copied_graph.edge_count, 3)
        self.assertListEqual(
            copied_graph.get_edges(),
            [
                ("A", "B", 0),
                ("B", "C", 1),
                ("C", "A", -1),
            ],
        )

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C", 1)
        self.undirected_graph.connect("C", "A", -1)

        copied_graph = self.undirected_graph.copy()
        self.assertEqual(copied_graph.vertex_count, 3)
        self.assertEqual(copied_graph.edge_count, 3)
        self.assertListEqual(
            copied_graph.get_edges(),
            [
                ("A", "B", 0),
                ("A", "C", -1),
                ("B", "A", 0),
                ("B", "C", 1),
                ("C", "A", -1),
                ("C", "B", 1),
            ],
        )

    def test_get_edges(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C", 1)
        self.directed_graph.connect("C", "A", -1)

        self.assertListEqual(
            self.directed_graph.get_edges(),
            [
                ("A", "B", 0),
                ("B", "C", 1),
                ("C", "A", -1),
            ],
        )

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C", 1)
        self.undirected_graph.connect("C", "A", -1)

        self.assertListEqual(
            self.undirected_graph.get_edges(),
            [
                ("A", "B", 0),
                ("A", "C", -1),
                ("B", "A", 0),
                ("B", "C", 1),
                ("C", "A", -1),
                ("C", "B", 1),
            ],
        )

    def test_get_predecessors(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C", 1)
        self.directed_graph.connect("C", "A", -1)

        self.assertListEqual(self.directed_graph.get_predecessors("A"), ["C"])
        self.assertListEqual(self.directed_graph.get_predecessors("B"), ["A"])
        self.assertListEqual(self.directed_graph.get_predecessors("C"), ["B"])
        self.assertRaises(VertexNotFoundError, self.directed_graph.get_predecessors, "D")

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C", 1)
        self.undirected_graph.connect("C", "A", -1)

        self.assertListEqual(self.undirected_graph.get_predecessors("A"), ["B", "C"])
        self.assertListEqual(self.undirected_graph.get_predecessors("B"), ["A", "C"])
        self.assertListEqual(self.undirected_graph.get_predecessors("C"), ["A", "B"])
        self.assertRaises(VertexNotFoundError, self.undirected_graph.get_predecessors, "D")

    def test_get_successors(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C", 1)
        self.directed_graph.connect("C", "A", -1)

        self.assertListEqual(self.directed_graph.get_successors("A"), ["B"])
        self.assertListEqual(self.directed_graph.get_successors("B"), ["C"])
        self.assertListEqual(self.directed_graph.get_successors("C"), ["A"])
        self.assertRaises(VertexNotFoundError, self.directed_graph.get_successors, "D")

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C", 1)
        self.undirected_graph.connect("C", "A", -1)

        self.assertListEqual(self.undirected_graph.get_successors("A"), ["B", "C"])
        self.assertListEqual(self.undirected_graph.get_successors("B"), ["A", "C"])
        self.assertListEqual(self.undirected_graph.get_successors("C"), ["A", "B"])
        self.assertRaises(VertexNotFoundError, self.undirected_graph.get_predecessors, "D")

    def test_get_neighbors(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.directed_graph.connect("A", "B")
        self.directed_graph.connect("B", "C", 1)
        self.directed_graph.connect("C", "A", -1)

        self.assertListEqual(self.directed_graph.get_neighbors("A"), ["C", "B"])
        self.assertListEqual(self.directed_graph.get_neighbors("B"), ["A", "C"])
        self.assertListEqual(self.directed_graph.get_neighbors("C"), ["B", "A"])
        self.assertRaises(VertexNotFoundError, self.directed_graph.get_neighbors, "D")

        self.undirected_graph.add_all(["A", "B", "C"])
        self.undirected_graph.connect("A", "B")
        self.undirected_graph.connect("B", "C", 1)
        self.undirected_graph.connect("C", "A", -1)

        self.assertListEqual(self.undirected_graph.get_neighbors("A"), ["B", "C"])
        self.assertListEqual(self.undirected_graph.get_neighbors("B"), ["A", "C"])
        self.assertListEqual(self.undirected_graph.get_neighbors("C"), ["A", "B"])
        self.assertRaises(VertexNotFoundError, self.undirected_graph.get_neighbors, "D")

    def test_is_directed(self) -> None:
        self.assertTrue(self.directed_graph.is_directed)
        self.assertFalse(self.undirected_graph.is_directed)

    def test_traverse_dfs(self) -> None:
        def _get_vertices(graph: IGraph[str, int], start: str) -> List[str]:
            vertices: List[str] = []
            graph.traverse(
                lambda vertex: vertices.append(vertex),
                GraphTraversalType.DEPTH_FIRST,
                start,
            )
            return vertices

        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
            graph.connect_all(
                [
                    ("A", "F", 0),
                    ("A", "B", 0),
                    ("A", "D", 0),
                    ("F", "A", 0),
                    ("F", "G", 0),
                    ("B", "C", 0),
                    ("D", "E", 0),
                    ("H", "I", 0),
                ]
            )

            self.assertListEqual(
                _get_vertices(graph, "A"),
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            )

            self.assertListEqual(
                _get_vertices(graph, "H"),
                ["H", "I", "A", "B", "C", "D", "E", "F", "G"],
            )

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_traverse_bfs(self) -> None:
        def _get_vertices(graph: IGraph[str, int], start: str) -> List[str]:
            vertices: List[str] = []
            graph.traverse(
                lambda vertex: vertices.append(vertex),
                GraphTraversalType.BREADTH_FIRST,
                start,
            )
            return vertices

        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
            graph.connect_all(
                [
                    ("A", "F", 0),
                    ("A", "B", 0),
                    ("A", "D", 0),
                    ("F", "A", 0),
                    ("F", "G", 0),
                    ("B", "C", 0),
                    ("D", "E", 0),
                    ("H", "I", 0),
                ]
            )

            self.assertListEqual(
                _get_vertices(graph, "A"),
                ["A", "B", "D", "F", "C", "E", "G", "H", "I"],
            )

            self.assertListEqual(
                _get_vertices(graph, "H"),
                ["H", "I", "A", "B", "D", "F", "C", "E", "G"],
            )

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_generator_dfs(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
            graph.connect_all(
                [
                    ("A", "F", 0),
                    ("A", "B", 0),
                    ("A", "D", 0),
                    ("F", "A", 0),
                    ("F", "G", 0),
                    ("B", "C", 0),
                    ("D", "E", 0),
                    ("H", "I", 0),
                ]
            )

            self.assertListEqual(
                [*graph.generator(GraphTraversalType.DEPTH_FIRST, "A")],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            )

            self.assertListEqual(
                [*graph.generator(GraphTraversalType.DEPTH_FIRST, "H")],
                ["H", "I", "A", "B", "C", "D", "E", "F", "G"],
            )

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_generator_bfs(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
            graph.connect_all(
                [
                    ("A", "F", 0),
                    ("A", "B", 0),
                    ("A", "D", 0),
                    ("F", "A", 0),
                    ("F", "G", 0),
                    ("B", "C", 0),
                    ("D", "E", 0),
                    ("H", "I", 0),
                ]
            )

            self.assertListEqual(
                [*graph.generator(GraphTraversalType.BREADTH_FIRST, "A")],
                ["A", "B", "D", "F", "C", "E", "G", "H", "I"],
            )

            self.assertListEqual(
                [*graph.generator(GraphTraversalType.BREADTH_FIRST, "H")],
                ["H", "I", "A", "B", "D", "F", "C", "E", "G"],
            )

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_is_connected(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            self.assertTrue(graph.is_connected)
            graph.add_all(["A", "B", "C", "D"])
            self.assertFalse(graph.is_connected)

            graph.connect("A", "B")
            self.assertFalse(graph.is_connected)

            graph.connect("B", "C")
            self.assertFalse(graph.is_connected)

            graph.connect("D", "C")
            self.assertTrue(graph.is_connected)

            graph.remove("B")
            self.assertFalse(graph.is_connected)

            graph.connect("A", "D")
            self.assertTrue(graph.is_connected)

            graph.disconnect("A", "D")
            self.assertFalse(graph.is_connected)

            graph.connect("A", "C")
            self.assertTrue(graph.is_connected)

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_is_cyclic(self) -> None:
        self.directed_graph.add_all(["A", "B", "C", "D"])
        self.assertFalse(self.directed_graph.is_cyclic)

        self.directed_graph.connect("A", "B")
        self.assertFalse(self.directed_graph.is_cyclic)

        self.directed_graph.connect("B", "C")
        self.assertFalse(self.directed_graph.is_cyclic)

        self.directed_graph.connect("C", "A")
        self.assertTrue(self.directed_graph.is_cyclic)

        self.directed_graph.connect("D", "C")
        self.assertTrue(self.directed_graph.is_cyclic)

        self.directed_graph.disconnect("C", "A")
        self.assertFalse(self.directed_graph.is_cyclic)

        self.directed_graph.connect("B", "D")
        self.assertFalse(self.directed_graph.is_cyclic)

        self.directed_graph.connect("D", "B")
        self.assertTrue(self.directed_graph.is_cyclic)

        self.directed_graph.disconnect("D", "B")
        self.assertFalse(self.directed_graph.is_cyclic)

        self.directed_graph.connect("D", "A")
        self.assertTrue(self.directed_graph.is_cyclic)

        self.undirected_graph.add_all(["A", "B", "C", "D"])
        self.assertFalse(self.undirected_graph.is_cyclic)

        self.undirected_graph.connect("A", "B")
        self.assertFalse(self.undirected_graph.is_cyclic)

        self.undirected_graph.connect("B", "C")
        self.assertFalse(self.undirected_graph.is_cyclic)

        self.undirected_graph.connect("C", "A")
        self.assertTrue(self.undirected_graph.is_cyclic)

        self.undirected_graph.connect("D", "B")
        self.assertTrue(self.undirected_graph.is_cyclic)

        self.undirected_graph.disconnect("C", "A")
        self.assertFalse(self.undirected_graph.is_cyclic)

    def test_get_path(self) -> None:
        def _test(graph: IGraph[str, int]) -> None:
            graph.add_all(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
            graph.connect_all(
                [
                    ("A", "F", 0),
                    ("A", "B", 0),
                    ("A", "D", 0),
                    ("F", "A", 0),
                    ("F", "G", 0),
                    ("B", "C", 0),
                    ("D", "E", 0),
                    ("H", "I", 0),
                ]
            )

            self.assertListEqual(graph.get_path("A", "C"), ["A", "B", "C"])
            self.assertListEqual(graph.get_path("A", "E"), ["A", "D", "E"])
            self.assertListEqual(graph.get_path("A", "G"), ["A", "F", "G"])
            self.assertListEqual(graph.get_path("A", "I"), [])
            self.assertListEqual(graph.get_path("A", "A"), ["A"])

        _test(self.directed_graph)
        _test(self.undirected_graph)

    def test_get_all_paths(self) -> None:
        self.directed_graph.add_all(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
        self.directed_graph.connect_all(
            [
                ("A", "F", 0),
                ("A", "B", 0),
                ("A", "D", 0),
                ("F", "A", 0),
                ("F", "G", 0),
                ("B", "C", 0),
                ("B", "E", 0),
                ("D", "E", 0),
                ("D", "C", 0),
                ("G", "E", 0),
                ("H", "I", 0),
            ]
        )
        self.assertListEqual(
            self.directed_graph.get_all_paths("A", "C"),
            [["A", "B", "C"], ["A", "D", "C"]],
        )

        self.assertListEqual(
            self.directed_graph.get_all_paths("A", "E"),
            [["A", "B", "E"], ["A", "D", "E"], ["A", "F", "G", "E"]],
        )

        self.assertListEqual(
            self.directed_graph.get_all_paths("A", "I"),
            [],
        )

        self.assertListEqual(
            self.directed_graph.get_all_paths("A", "A"),
            [["A"]],
        )

        self.undirected_graph.add_all(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
        self.undirected_graph.connect_all(
            [
                ("A", "F", 0),
                ("A", "B", 0),
                ("A", "D", 0),
                ("F", "A", 0),
                ("F", "G", 0),
                ("B", "C", 0),
                ("B", "E", 0),
                ("D", "E", 0),
                ("D", "C", 0),
                ("G", "E", 0),
                ("H", "I", 0),
            ]
        )

        self.assertListEqual(
            self.undirected_graph.get_all_paths("A", "C"),
            [
                ["A", "B", "C"],
                ["A", "B", "E", "D", "C"],
                ["A", "D", "C"],
                ["A", "D", "E", "B", "C"],
                ["A", "F", "G", "E", "B", "C"],
                ["A", "F", "G", "E", "D", "C"],
            ],
        )

        self.assertListEqual(
            self.undirected_graph.get_all_paths("A", "F"),
            [
                ["A", "B", "C", "D", "E", "G", "F"],
                ["A", "B", "E", "G", "F"],
                ["A", "D", "C", "B", "E", "G", "F"],
                ["A", "D", "E", "G", "F"],
                ["A", "F"],
            ],
        )

        self.assertListEqual(
            self.undirected_graph.get_all_paths("A", "I"),
            [],
        )

        self.assertListEqual(
            self.undirected_graph.get_all_paths("A", "A"),
            [["A"]],
        )


class GraphSerializationTests(unittest.TestCase):
    @dataclass
    @total_ordering
    class Item:
        value: int
        some_text: str = "default"

        def __lt__(self, other: GraphSerializationTests.Item) -> bool:
            return self.value < other.value

        def __eq__(self, other: object) -> bool:
            return isinstance(other, GraphSerializationTests.Item) and self.value == other.value

    @override
    def setUp(self) -> None:
        self.directed_graph_filename: str = "directed_graph.json"
        self.undirected_graph_filename: str = "undirected_graph.json"

    @override
    def tearDown(self) -> None:
        try:
            import os

            os.remove(self.directed_graph_filename)
            os.remove(self.undirected_graph_filename)
        except FileNotFoundError:
            pass

    def test_literal_in_adjacency_matrix_graph(self) -> None:
        def _test(graph: AdjacencyMatrixGraph[str, int], filename: str) -> None:
            graph.add_all(["A", "B", "C", "D", "E"])
            graph.connect_all(
                [
                    ("A", "B", 1),
                    ("A", "C", 2),
                    ("B", "D", 3),
                    ("C", "E", 4),
                    ("D", "E", 5),
                ]
            )

            GraphSerializer.save_graph_to_file(graph, filename)

            graph_copy: AdjacencyMatrixGraph[str, int] = graph.copy()
            graph_copy.clear()

            GraphSerializer.load_graph_from_file(graph_copy, filename, str)

            self.assertListEqual(graph.get_edges(), graph_copy.get_edges())

        _test(AdjacencyMatrixGraph[str, int](True), self.directed_graph_filename)
        _test(AdjacencyMatrixGraph[str, int](False), self.undirected_graph_filename)

    def test_item_in_adjacency_matrix_graph(self) -> None:
        def _test(
            graph: AdjacencyMatrixGraph[GraphSerializationTests.Item, int], filename: str
        ) -> None:
            graph.add_all(
                [
                    GraphSerializationTests.Item(1, "one"),
                    GraphSerializationTests.Item(2, "two"),
                    GraphSerializationTests.Item(3, "three"),
                    GraphSerializationTests.Item(4, "four"),
                    GraphSerializationTests.Item(5, "five"),
                ]
            )
            graph.connect_all(
                [
                    (GraphSerializationTests.Item(1), GraphSerializationTests.Item(2), 1),
                    (GraphSerializationTests.Item(1), GraphSerializationTests.Item(3), 2),
                    (GraphSerializationTests.Item(2), GraphSerializationTests.Item(4), 3),
                    (GraphSerializationTests.Item(3), GraphSerializationTests.Item(5), 4),
                    (GraphSerializationTests.Item(4), GraphSerializationTests.Item(5), 5),
                ]
            )

            GraphSerializer.save_graph_to_file(graph, filename)

            graph_copy: AdjacencyMatrixGraph[GraphSerializationTests.Item, int] = graph.copy()
            graph_copy.clear()

            GraphSerializer.load_graph_from_file(graph_copy, filename, GraphSerializationTests.Item)

            self.assertListEqual(graph.get_edges(), graph_copy.get_edges())

        _test(
            AdjacencyMatrixGraph[GraphSerializationTests.Item, int](True),
            self.directed_graph_filename,
        )
        _test(
            AdjacencyMatrixGraph[GraphSerializationTests.Item, int](False),
            self.undirected_graph_filename,
        )


class GraphAlgsTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.directed_graph: AdjacencyMatrixGraph[str, int] = AdjacencyMatrixGraph(is_directed=True)
        self.undirected_graph: AdjacencyMatrixGraph[str, int] = AdjacencyMatrixGraph(
            is_directed=False
        )

    def test_directed_graph_dijkstra(self) -> None:
        self.directed_graph.add_all(["X1", "X2", "X3", "X4", "X5", "X6", "X7"])

        self.directed_graph.connect_all(
            [
                ("X1", "X3", 11),
                ("X1", "X4", 15),
                ("X1", "X5", 7),
                ("X2", "X5", 14),
                ("X2", "X6", 18),
                ("X3", "X2", 9),
                ("X3", "X4", 13),
                ("X3", "X5", 7),
                ("X3", "X6", 11),
                ("X3", "X7", 22),
                ("X4", "X6", 11),
                ("X4", "X7", 16),
                ("X5", "X6", 8),
                ("X5", "X7", 23),
                ("X6", "X7", 19),
            ]
        )

        self.assertEqual(dijkstra(self.directed_graph, "X1", "X7"), (["X1", "X5", "X7"], 30))

        self.directed_graph.clear()
        self.directed_graph.add_all(["X1", "X2", "X3"])
        self.assertEqual(dijkstra(self.directed_graph, "X1", "X3"), None)

        self.directed_graph.connect_all([("X1", "X2", 5), ("X2", "X3", 5), ("X3", "X1", -1)])
        self.assertEqual(dijkstra(self.directed_graph, "X1", "X3"), (["X1", "X2", "X3"], 10))

        self.directed_graph.connect("X1", "X3", -1)
        self.assertRaises(NegativeWeightException, dijkstra, self.directed_graph, "X1", "X3")

        self.directed_graph.clear()
        self.directed_graph.add_all(["X1", "X2", "X3", "X4"])
        self.directed_graph.connect_all(
            [
                ("X1", "X3", 1),
                ("X1", "X2", 0),
                ("X2", "X4", 2),
                ("X3", "X4", 2),
            ]
        )
        self.assertEqual(dijkstra(self.directed_graph, "X1", "X4"), (["X1", "X2", "X4"], 2))

    def test_undirected_graph_dijkstra(self) -> None:
        self.undirected_graph.add_all(["X1", "X2", "X3", "X4", "X5", "X6"])

        self.undirected_graph.connect_all(
            [
                ("X1", "X2", 7),
                ("X1", "X3", 9),
                ("X1", "X6", 14),
                ("X2", "X3", 10),
                ("X2", "X4", 15),
                ("X3", "X6", 2),
                ("X3", "X4", 11),
                ("X4", "X5", 6),
                ("X6", "X5", 9),
            ]
        )

        self.assertEqual(
            dijkstra(self.undirected_graph, "X1", "X5"), (["X1", "X3", "X6", "X5"], 20)
        )

        self.undirected_graph.clear()
        self.undirected_graph.add_all(["X1", "X2", "X3"])
        self.assertEqual(dijkstra(self.undirected_graph, "X1", "X3"), None)

        self.undirected_graph.connect_all([("X1", "X2", 5), ("X2", "X3", 5), ("X3", "X1", -1)])
        self.assertRaises(NegativeWeightException, dijkstra, self.undirected_graph, "X1", "X3")

        self.undirected_graph.connect("X3", "X1", 1)
        self.assertEqual(dijkstra(self.undirected_graph, "X1", "X3"), (["X1", "X3"], 1))

        self.undirected_graph.clear()
        self.undirected_graph.add_all(["X1", "X2", "X3", "X4"])
        self.undirected_graph.connect_all(
            [
                ("X1", "X3", 1),
                ("X1", "X2", 0),
                ("X2", "X4", 2),
                ("X3", "X4", 2),
            ]
        )
        self.assertEqual(dijkstra(self.undirected_graph, "X1", "X4"), (["X1", "X2", "X4"], 2))

    def test_topological_sort(self) -> None:
        self.directed_graph.add_all(["A", "B", "C"])
        self.assertListEqual(["A", "B", "C"], topological_sort(self.directed_graph))

        self.directed_graph.connect_all(
            [
                ("A", "B", 0),
                ("B", "C", 0),
            ]
        )
        self.assertListEqual(["C", "B", "A"], topological_sort(self.directed_graph))

        self.directed_graph.disconnect_all(
            [
                ("A", "B"),
                ("B", "C"),
            ]
        )
        self.directed_graph.add_all(["D", "E"])
        self.directed_graph.connect_all(
            [
                ("A", "B", 0),
                ("B", "C", 0),
                ("A", "D", 0),
                ("D", "E", 0),
            ]
        )
        self.assertListEqual(["C", "B", "E", "D", "A"], topological_sort(self.directed_graph))

        self.directed_graph.clear()
        self.directed_graph.add_all(["X1", "X2", "X3", "X4"])
        self.directed_graph.connect_all(
            [
                ("X1", "X4", 0),
                ("X4", "X2", 0),
                ("X4", "X3", 0),
                ("X3", "X2", 0),
            ]
        )
        self.assertListEqual(["X2", "X3", "X4", "X1"], topological_sort(self.directed_graph))

        self.directed_graph.connect("X2", "X1", 0)
        self.assertRaises(CycleInGraphException, topological_sort, self.directed_graph)

        self.assertRaises(NotDirectedGraphException, topological_sort, self.undirected_graph)


if __name__ == "__main__":
    unittest.main()
