import unittest
from typing import List

from common.extra_typing import override
from lab6.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from lab6.graph.graph import (
    GraphTraversalType,
    IGraph,
    SelfConnectionError,
    VertexNotFoundError,
)


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


if __name__ == "__main__":
    unittest.main()
