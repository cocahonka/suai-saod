from __future__ import annotations

from dataclasses import dataclass
from random import randint
from typing import Callable, Final, Generic, Iterator, Optional, Tuple

from common.comparable import Comparable
from common.extra_typing import override
from lab3.models.number import *
from lab3.models.student import *
from lab3.trees.trie import *


@dataclass
class TernaryTrieNode(Generic[K, V]):
    key_piece: Comparable
    key: Optional[K] = None
    value: Optional[V] = None
    left: Optional[TernaryTrieNode[K, V]] = None
    middle: Optional[TernaryTrieNode[K, V]] = None
    right: Optional[TernaryTrieNode[K, V]] = None

    @property
    def is_key(self) -> bool:
        return self.value is not None and self.key is not None


class TernaryTrie(ITrie[K, V], Generic[K, V]):
    def __init__(self) -> None:
        self._root: Optional[TernaryTrieNode[K, V]] = None
        self._size: int = 0

    @override
    @property
    def size(self) -> int:
        return self._size

    @override
    def put(self, key: K, value: V) -> None:
        if not key:
            return

        self._root = self._put(self._root, key, value, 0)

    def _put(
        self,
        node: Optional[TernaryTrieNode[K, V]],
        key: K,
        value: Optional[V],
        index: int,
    ) -> TernaryTrieNode[K, V]:
        key_piece: Final[Comparable] = key[index]

        if node is None:
            node = TernaryTrieNode(key_piece)

        if key_piece < node.key_piece:
            node.left = self._put(node.left, key, value, index)
        elif key_piece > node.key_piece:
            node.right = self._put(node.right, key, value, index)
        elif index < len(key) - 1:
            node.middle = self._put(node.middle, key, value, index + 1)
        else:
            if node.value is None:
                self._size += 1
            node.value = value
            node.key = key

        return node

    @override
    def get_or_none(self, key: K) -> Optional[V]:
        if not key:
            return None

        node: Final[Optional[TernaryTrieNode[K, V]]] = self._get(self._root, key, 0)
        return node.value if node is not None and node.is_key else None

    def _get(
        self,
        node: Optional[TernaryTrieNode[K, V]],
        key: K,
        index: int,
    ) -> Optional[TernaryTrieNode[K, V]]:
        if node is None:
            return None

        key_piece: Final[Comparable] = key[index]

        if key_piece < node.key_piece:
            return self._get(node.left, key, index)
        if key_piece > node.key_piece:
            return self._get(node.right, key, index)
        if index < len(key) - 1:
            return self._get(node.middle, key, index + 1)

        return node

    @override
    def keys_with_prefix(self, prefix: K) -> Iterator[K]:
        if not prefix:
            return

        node: Final[Optional[TernaryTrieNode[K, V]]] = self._get(self._root, prefix, 0)
        if node is None:
            return

        if node.is_key:
            assert node.key is not None
            yield node.key

        yield from (key for key, _ in self._in_order_generator(node.middle))

    @override
    def longest_prefix_of(self, query: K) -> Optional[K]:
        if not query:
            return None

        length: Final[int] = self._longest_prefix_of(self._root, query, 0, 0)
        return query[:length] if length > 0 else None

    def _longest_prefix_of(
        self,
        node: Optional[TernaryTrieNode[K, V]],
        query: K,
        index: int,
        length: int,
    ) -> int:
        if node is None:
            return length

        key_piece: Final[Comparable] = query[index]

        if key_piece < node.key_piece:
            return self._longest_prefix_of(node.left, query, index, length)
        if key_piece > node.key_piece:
            return self._longest_prefix_of(node.right, query, index, length)
        if node.is_key:
            length = index + 1
        if index < len(query) - 1:
            return self._longest_prefix_of(node.middle, query, index + 1, length)

        return length

    @override
    def delete(self, key: K) -> bool:
        if not self.contains(key):
            return False

        self._root = self._put(self._root, key, None, 0)
        self._size -= 1
        return True

    @override
    def clear(self) -> None:
        self._root = None
        self._size = 0

    @override
    def traverse(
        self,
        action: Callable[[K, V], None],
        traverse_type: TraverseType = TraverseType.IN_ORDER,
    ) -> None:
        match traverse_type:
            case TraverseType.PRE_ORDER:
                self._pre_order_traverse(self._root, action)
            case TraverseType.IN_ORDER:
                self._in_order_traverse(self._root, action)
            case TraverseType.POST_ORDER:
                self._post_order_traverse(self._root, action)

    def _pre_order_traverse(
        self, node: Optional[TernaryTrieNode[K, V]], action: Callable[[K, V], None]
    ) -> None:
        if node is None:
            return
        if node.is_key:
            assert node.key is not None and node.value is not None
            action(node.key, node.value)

        self._pre_order_traverse(node.left, action)
        self._pre_order_traverse(node.middle, action)
        self._pre_order_traverse(node.right, action)

    def _in_order_traverse(
        self, node: Optional[TernaryTrieNode[K, V]], action: Callable[[K, V], None]
    ) -> None:
        if node is None:
            return

        self._in_order_traverse(node.left, action)
        if node.is_key:
            assert node.key is not None and node.value is not None
            action(node.key, node.value)
        self._in_order_traverse(node.middle, action)
        self._in_order_traverse(node.right, action)

    def _post_order_traverse(
        self, node: Optional[TernaryTrieNode[K, V]], action: Callable[[K, V], None]
    ) -> None:
        if node is None:
            return

        self._post_order_traverse(node.left, action)
        self._post_order_traverse(node.middle, action)
        self._post_order_traverse(node.right, action)
        if node.is_key:
            assert node.key is not None and node.value is not None
            action(node.key, node.value)

    @override
    def generator(
        self, traverse_type: TraverseType = TraverseType.IN_ORDER
    ) -> Iterator[Tuple[K, V]]:
        match traverse_type:
            case TraverseType.PRE_ORDER:
                yield from self._pre_order_generator(self._root)
            case TraverseType.IN_ORDER:
                yield from self._in_order_generator(self._root)
            case TraverseType.POST_ORDER:
                yield from self._post_order_generator(self._root)

    def _pre_order_generator(self, node: Optional[TernaryTrieNode[K, V]]) -> Iterator[Tuple[K, V]]:
        if node is None:
            return

        if node.is_key:
            assert node.key is not None and node.value is not None
            yield node.key, node.value

        yield from self._pre_order_generator(node.left)
        yield from self._pre_order_generator(node.middle)
        yield from self._pre_order_generator(node.right)

    def _in_order_generator(self, node: Optional[TernaryTrieNode[K, V]]) -> Iterator[Tuple[K, V]]:
        if node is None:
            return

        yield from self._in_order_generator(node.left)
        if node.is_key:
            assert node.key is not None and node.value is not None
            yield node.key, node.value
        yield from self._in_order_generator(node.middle)
        yield from self._in_order_generator(node.right)

    def _post_order_generator(self, node: Optional[TernaryTrieNode[K, V]]) -> Iterator[Tuple[K, V]]:
        if node is None:
            return

        yield from self._post_order_generator(node.left)
        yield from self._post_order_generator(node.middle)
        yield from self._post_order_generator(node.right)
        if node.is_key:
            assert node.key is not None and node.value is not None
            yield node.key, node.value

    @override
    def __str__(self) -> str:
        return f"TernaryTrie({', '.join(f'{key}: {value}' for key, value in self.generator())})"
