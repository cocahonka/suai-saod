from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar

from lab6.graph.graph import GraphTraversalType, IGraph, Weight

T = TypeVar("T")


class GraphSerializer:
    @classmethod
    def save_graph_to_file(cls, graph: IGraph[T, Weight], filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            vertices: List[T] = [*graph.generator(traverse_type=GraphTraversalType.BREADTH_FIRST)]
            edges: List[Tuple[T, T, Optional[Weight]]] = graph.get_edges()

            data: Dict[str, Any] = {
                "vertices": [cls.node_to_dict(vertex) for vertex in vertices],
                "edges": [
                    [
                        cls.node_to_dict(from_vertex),
                        cls.node_to_dict(to_vertex),
                        weight,
                    ]
                    for from_vertex, to_vertex, weight in edges
                ],
            }

            json.dump(data, file, ensure_ascii=False, indent=4)

    @classmethod
    def load_graph_from_file(
        cls,
        graph: IGraph[T, Weight],
        filename: str,
        data_type: Type[T],
    ) -> None:
        graph.clear()

        with open(filename, "r", encoding="utf-8") as file:
            data: Dict[str, Any] = json.load(file)

            vertices: List[T] = [cls.dict_to_node(vertex, data_type) for vertex in data["vertices"]]
            edges: List[Tuple[T, T, Weight]] = [
                (
                    cls.dict_to_node(from_vertex, data_type),
                    cls.dict_to_node(to_vertex, data_type),
                    weight,
                )
                for from_vertex, to_vertex, weight in data["edges"]
            ]

        graph.add_all(vertices)
        graph.connect_all(edges)

    @classmethod
    def node_to_dict(cls, node: T) -> object:
        if isinstance(node, (int, float, str)):
            return node
        if hasattr(node, "__dict__"):
            return node.__dict__
        raise ValueError(f"Unsupported type {type(node)} for JSON serialization")

    @classmethod
    def dict_to_node(cls, data: Dict[str, Any], class_type: Type[T]) -> T:
        if isinstance(data, dict):
            return class_type(**data)
        return data
