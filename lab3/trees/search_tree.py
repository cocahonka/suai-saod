from __future__ import annotations

from typing import Callable, Final, Generic, Iterator, List, Optional

from common.extra_typing import contravariant_args, override
from lab3.trees.ordered_binary_tree import (
    BinaryNode,
    IOrderedBinaryTree,
    OrderedBinaryTreeEmptyException,
    T,
    TraversalType,
)


class SearchTree(IOrderedBinaryTree[T], Generic[T]):
    def __init__(self) -> None:
        self._root: Optional[BinaryNode[T]] = None
        self._size: int = 0

    @override
    @property
    def size(self) -> int:
        return self._size

    @override
    def insert(self, value: T) -> None:
        node: Final[BinaryNode[T]] = BinaryNode(value)
        if self._root is None:
            self._root = node
            self._size += 1
        else:
            self._insert(self._root, node)

    @contravariant_args
    def _insert(self, parent: BinaryNode[T], new_node: BinaryNode[T]) -> None:
        if new_node.value > parent.value:
            if parent.right is None:
                parent.right = new_node
                self._size += 1
            self._insert(parent.right, new_node)
        elif new_node.value < parent.value:
            if parent.left is None:
                parent.left = new_node
                self._size += 1
            self._insert(parent.left, new_node)

    @override
    def contains(self, value: T) -> bool:
        return self._contains(self._root, value)

    def _contains(self, node: Optional[BinaryNode[T]], value: T) -> bool:
        if node is None:
            return False
        if node.value == value:
            return True
        return self._contains(node.right if value > node.value else node.left, value)

    @override
    def find_max(self) -> T:
        return self._find_max(self._root)

    def _find_max(self, node: Optional[BinaryNode[T]]) -> T:
        if node is None:
            raise OrderedBinaryTreeEmptyException("Tree is empty")
        if node.right is None:
            return node.value
        return self._find_max(node.right)

    @override
    def find_min(self) -> T:
        return self._find_min(self._root)

    def _find_min(self, node: Optional[BinaryNode[T]]) -> T:
        if node is None:
            raise OrderedBinaryTreeEmptyException("Tree is empty")
        if node.left is None:
            return node.value
        return self._find_min(node.left)

    @override
    def delete(self, value: T) -> None:
        self._root = self._delete(self._root, value)

    @contravariant_args
    def _delete(self, parent: Optional[BinaryNode[T]], value: T) -> Optional[BinaryNode[T]]:
        if parent is None:
            return None
        if value > parent.value:
            parent.right = self._delete(parent.right, value)
        elif value < parent.value:
            parent.left = self._delete(parent.left, value)
        else:
            if parent.left is None:
                self._size -= 1
                return parent.right
            if parent.right is None:
                self._size -= 1
                return parent.left
            parent.value = self._find_max(parent.left)
            parent.left = self._delete(parent.left, parent.value)
        return parent

    @override
    def clear(self) -> None:
        self._root = None
        self._size = 0

    @override
    def traverse(
        self,
        action: Callable[[T], None],
        traverse_type: TraversalType = TraversalType.IN_ORDER,
    ) -> None:
        match traverse_type:
            case TraversalType.PRE_ORDER:
                self._pre_order(self._root, action)
            case TraversalType.IN_ORDER:
                self._in_order(self._root, action)
            case TraversalType.POST_ORDER:
                self._post_order(self._root, action)

    def _pre_order(self, node: Optional[BinaryNode[T]], action: Callable[[T], None]) -> None:
        if node is None:
            return
        action(node.value)
        self._pre_order(node.left, action)
        self._pre_order(node.right, action)

    def _in_order(self, node: Optional[BinaryNode[T]], action: Callable[[T], None]) -> None:
        if node is None:
            return
        self._in_order(node.left, action)
        action(node.value)
        self._in_order(node.right, action)

    def _post_order(self, node: Optional[BinaryNode[T]], action: Callable[[T], None]) -> None:
        if node is None:
            return
        self._post_order(node.left, action)
        self._post_order(node.right, action)
        action(node.value)

    @override
    def generator(self, traverse_type: TraversalType = TraversalType.IN_ORDER) -> Iterator[T]:
        match traverse_type:
            case TraversalType.PRE_ORDER:
                yield from self._pre_order_generator(self._root)
            case TraversalType.IN_ORDER:
                yield from self._in_order_generator(self._root)
            case TraversalType.POST_ORDER:
                yield from self._post_order_generator(self._root)

    def _pre_order_generator(self, node: Optional[BinaryNode[T]]) -> Iterator[T]:
        if node is None:
            return
        yield node.value
        yield from self._pre_order_generator(node.left)
        yield from self._pre_order_generator(node.right)

    def _in_order_generator(self, node: Optional[BinaryNode[T]]) -> Iterator[T]:
        if node is None:
            return
        yield from self._in_order_generator(node.left)
        yield node.value
        yield from self._in_order_generator(node.right)

    def _post_order_generator(self, node: Optional[BinaryNode[T]]) -> Iterator[T]:
        if node is None:
            return
        yield from self._post_order_generator(node.left)
        yield from self._post_order_generator(node.right)
        yield node.value

    @override
    def __str__(self) -> str:
        class_name: Final[str] = self.__class__.__name__
        if self._root is None:
            return f"{class_name} is empty"
        result: List[str] = [f"{class_name}\n"]
        self._create_str_tree(result, "", self._root, True)
        return "".join(result)

    def _create_str_tree(
        self,
        result: List[str],
        prefix: str,
        node: BinaryNode[T],
        is_tail: bool,
    ) -> None:
        if node.right is not None:
            new_prefix = prefix + ("│   " if is_tail else "    ")
            self._create_str_tree(result, new_prefix, node.right, False)

        result.append(prefix + ("└── " if is_tail else "┌── ") + str(node.value) + "\n")

        if node.left is not None:
            new_prefix = prefix + ("    " if is_tail else "│   ")
            self._create_str_tree(result, new_prefix, node.left, True)
