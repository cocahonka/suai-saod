from __future__ import annotations

import json
from typing import Any, Dict, List, Type, Union

from lab3.trees.ordered_binary_tree import IOrderedBinaryTree, T, TraversalType


class OrderedBinaryTreeSerializer:
    _Result = Union[Dict[str, Any], T, int, float, str]

    @staticmethod
    def save_tree_to_file(tree: IOrderedBinaryTree[T], filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            data: List[OrderedBinaryTreeSerializer._Result[T]] = [
                OrderedBinaryTreeSerializer.node_to_dict(node)
                for node in tree.generator(traverse_type=TraversalType.PRE_ORDER)
            ]
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_tree_from_file(tree: IOrderedBinaryTree[T], filename: str, data_type: Type[T]) -> None:
        tree.clear()
        with open(filename, "r", encoding="utf-8") as f:
            data: List[Union[Dict[str, Any], T]] = json.load(f)
            nodes: List[T] = [
                OrderedBinaryTreeSerializer.dict_to_node(d, data_type) if isinstance(d, dict) else d
                for d in data
            ]
        for item in nodes:
            tree.insert(item)

    @staticmethod
    def node_to_dict(node: T) -> OrderedBinaryTreeSerializer._Result[T]:
        if isinstance(node, (int, float, str)):
            return node
        elif hasattr(node, "__dict__"):
            return node.__dict__
        raise ValueError(f"Unsupported type {type(node)} for JSON serialization")

    @staticmethod
    def dict_to_node(data: Union[Dict[str, Any], T], cls: Type[T]) -> T:
        if isinstance(data, dict):
            return cls(**data)
        return data
