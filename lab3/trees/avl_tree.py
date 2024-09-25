from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Generic, Optional, cast

from common.extra_typing import contravariant_args, override
from lab3.trees.ordered_binary_tree import BinaryNode, T
from lab3.trees.search_tree import SearchTree


@dataclass
class AVLNode(BinaryNode[T], Generic[T]):
    height: int = 0
    left: Optional[AVLNode[T]] = None
    right: Optional[AVLNode[T]] = None


class AVLTree(SearchTree[T], Generic[T]):
    def __init__(self) -> None:
        self._root: Optional[AVLNode[T]] = None
        self._size: int = 0

    def _get_height(self, node: Optional[AVLNode[T]]) -> int:
        return -1 if node is None else node.height

    def _update_height(self, node: AVLNode[T]) -> None:
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _get_balance(self, node: Optional[AVLNode[T]]) -> int:
        return 0 if node is None else self._get_height(node.right) - self._get_height(node.left)

    def _swap(self, first: AVLNode[T], second: AVLNode[T]) -> None:
        first.value, second.value = second.value, first.value

    def _right_rotate(self, node: AVLNode[T]) -> None:
        assert node.left is not None
        self._swap(node, node.left)
        right: Final[Optional[AVLNode[T]]] = node.right
        node.right = node.left
        node.left = node.right.left
        node.right.left = node.right.right
        node.right.right = right
        self._update_height(node.right)
        self._update_height(node)

    def _left_rotate(self, node: AVLNode[T]) -> None:
        assert node.right is not None
        self._swap(node, node.right)
        left: Final[Optional[AVLNode[T]]] = node.left
        node.left = node.right
        node.right = node.left.right
        node.left.right = node.left.left
        node.left.left = left
        self._update_height(node.left)
        self._update_height(node)

    def _balance(self, node: AVLNode[T]) -> None:
        balance: Final[int] = self._get_balance(node)

        if balance == -2:
            if self._get_balance(node.left) == 1:
                assert node.left is not None
                self._left_rotate(node.left)
            self._right_rotate(node)
        elif balance == 2:
            if self._get_balance(node.right) == -1:
                assert node.right is not None
                self._right_rotate(node.right)
            self._left_rotate(node)

    @override
    def insert(self, value: T) -> None:
        node: Final[AVLNode[T]] = AVLNode(value)
        if self._root is None:
            self._root = node
            self._size += 1
        else:
            self._insert(self._root, node)

    @override
    @contravariant_args
    def _insert(self, parent: AVLNode[T], new_node: AVLNode[T]) -> None:  # type: ignore[override]
        super()._insert(parent, new_node)  # indirect recursion

        self._update_height(parent)
        self._balance(parent)

    @override
    @contravariant_args
    def _delete(self, parent: Optional[AVLNode[T]], value: T) -> Optional[AVLNode[T]]:  # type: ignore[override]
        parent = cast(Optional[AVLNode[T]], super()._delete(parent, value))  # indirect recursion

        if parent is not None:
            self._update_height(parent)
            self._balance(parent)

        return parent
