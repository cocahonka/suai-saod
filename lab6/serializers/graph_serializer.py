from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union, cast

from lab6.graph.graph import IGraph, Weight

T = TypeVar("T")


class GraphSerializer:
    @classmethod
    def save_graph_to_file(cls, graph: IGraph[T, Weight], filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            edges: List[Tuple[T, T, Optional[Weight]]] = graph.get_edges()

            data: Dict[str, Any] = {
                "edges": [[cls.node_to_dict(u), cls.node_to_dict(v), w] for u, v, w in edges]
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
            edges: List[Tuple[T, T, Optional[Weight]]] = [
                (cls.dict_to_node(u, data_type), cls.dict_to_node(v, data_type), w)
                for u, v, w in data["edges"]
            ]

        for u, v, _ in edges:
            graph.add(u)
            graph.add(v)

        for u, v, w in edges:
            graph.connect(u, v, cast(Weight, w))

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
