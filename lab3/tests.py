from __future__ import annotations

import unittest
from dataclasses import dataclass
from functools import total_ordering
from typing import Any, List, Tuple

from common.extra_typing import override
from lab3.serializers.ordered_binary_tree_serializer import OrderedBinaryTreeSerializer
from lab3.trees.avl_tree import AVLTree
from lab3.trees.ordered_binary_tree import (
    IOrderedBinaryTree,
    OrderedBinaryTreeEmptyException,
    T,
    TraversalType,
)
from lab3.trees.search_tree import SearchTree
from lab3.trees.ternary_trie import TernaryTrie, TraverseType, TrieElementNotFound
from lab3.trees.trie import ITrie


def _get_pre_order_tree(tree: IOrderedBinaryTree[T]) -> List[T]:
    return [*tree.generator(TraversalType.PRE_ORDER)]


def _get_in_order_tree(tree: IOrderedBinaryTree[T]) -> List[T]:
    return [*tree.generator(TraversalType.IN_ORDER)]


def _get_post_order_tree(tree: IOrderedBinaryTree[T]) -> List[T]:
    return [*tree.generator(TraversalType.POST_ORDER)]


class SearchTreeTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.tree: IOrderedBinaryTree[int] = SearchTree()

    def test_size(self) -> None:
        self.assertEqual(self.tree.size, 0)
        self.tree.insert(1)
        self.assertEqual(self.tree.size, 1)

    def test_insert(self) -> None:
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.insert(5)
        self.assertEqual(self.tree.size, 3)
        self.assertListEqual(_get_pre_order_tree(self.tree), [1, 3, 5])
        self.assertListEqual(_get_in_order_tree(self.tree), [1, 3, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [5, 3, 1])
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        self.assertListEqual(_get_pre_order_tree(self.tree), [1, -1, 3, 2, 5, 4])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 1, 2, 3, 4, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [-1, 2, 4, 5, 3, 1])

    def test_contains(self) -> None:
        self.assertFalse(self.tree.contains(1))
        self.tree.insert(1)
        self.assertTrue(self.tree.contains(1))
        self.assertFalse(self.tree.contains(2))
        self.tree.insert(2)
        self.assertTrue(self.tree.contains(2))

    def test_find_max(self) -> None:
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_max)
        self.tree.insert(1)
        self.assertEqual(self.tree.find_max(), 1)
        self.tree.insert(3)
        self.assertEqual(self.tree.find_max(), 3)
        self.tree.insert(5)
        self.assertEqual(self.tree.find_max(), 5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        self.assertEqual(self.tree.find_max(), 5)

    def test_find_min(self) -> None:
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_min)
        self.tree.insert(1)
        self.assertEqual(self.tree.find_min(), 1)
        self.tree.insert(3)
        self.assertEqual(self.tree.find_min(), 1)
        self.tree.insert(5)
        self.assertEqual(self.tree.find_min(), 1)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        self.assertEqual(self.tree.find_min(), -1)

    def test_delete(self) -> None:
        self.tree.insert(1)
        self.tree.delete(1)
        self.assertEqual(self.tree.size, 0)
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        self.tree.delete(1)
        self.assertListEqual(_get_pre_order_tree(self.tree), [-1, 3, 2, 5, 4])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2, 3, 4, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [2, 4, 5, 3, -1])
        self.tree.delete(3)
        self.assertListEqual(_get_pre_order_tree(self.tree), [-1, 2, 5, 4])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2, 4, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [4, 5, 2, -1])
        self.tree.delete(4)
        self.assertListEqual(_get_pre_order_tree(self.tree), [-1, 2, 5])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [5, 2, -1])
        self.tree.delete(5)
        self.assertListEqual(_get_pre_order_tree(self.tree), [-1, 2])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2])
        self.assertListEqual(_get_post_order_tree(self.tree), [2, -1])
        self.tree.delete(-1)
        self.assertListEqual(_get_pre_order_tree(self.tree), [2])
        self.assertListEqual(_get_in_order_tree(self.tree), [2])
        self.assertListEqual(_get_post_order_tree(self.tree), [2])
        self.tree.delete(2)
        self.assertEqual(self.tree.size, 0)

    def test_clear(self) -> None:
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.clear()
        self.assertEqual(self.tree.size, 0)
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_max)
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_min)

    def test_traverse(self) -> None:
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        pre_order: List[int] = []
        in_order: List[int] = []
        post_order: List[int] = []
        self.tree.traverse(lambda x: pre_order.append(x), TraversalType.PRE_ORDER)
        self.tree.traverse(lambda x: in_order.append(x), TraversalType.IN_ORDER)
        self.tree.traverse(lambda x: post_order.append(x), TraversalType.POST_ORDER)
        self.assertListEqual(pre_order, [1, -1, 3, 2, 5, 4])
        self.assertListEqual(in_order, [-1, 1, 2, 3, 4, 5])
        self.assertListEqual(post_order, [-1, 2, 4, 5, 3, 1])

    def test_generator(self) -> None:
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        pre_order: List[int] = [*self.tree.generator(TraversalType.PRE_ORDER)]
        in_order: List[int] = [*self.tree.generator(TraversalType.IN_ORDER)]
        post_order: List[int] = [*self.tree.generator(TraversalType.POST_ORDER)]
        self.assertListEqual(pre_order, [1, -1, 3, 2, 5, 4])
        self.assertListEqual(in_order, [-1, 1, 2, 3, 4, 5])
        self.assertListEqual(post_order, [-1, 2, 4, 5, 3, 1])


class AVLTreeTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.tree: IOrderedBinaryTree[int] = AVLTree()

    def test_size(self) -> None:
        self.assertEqual(self.tree.size, 0)
        self.tree.insert(1)
        self.assertEqual(self.tree.size, 1)

    def test_insert(self) -> None:
        # right rotation
        self.tree.insert(4)
        self.tree.insert(2)
        self.tree.insert(1)
        self.tree.insert(1)
        self.assertEqual(self.tree.size, 3)
        self.assertListEqual(_get_pre_order_tree(self.tree), [2, 1, 4])
        self.assertListEqual(_get_in_order_tree(self.tree), [1, 2, 4])
        self.assertListEqual(_get_post_order_tree(self.tree), [1, 4, 2])
        # left rotation
        self.tree.insert(6)
        self.tree.insert(7)
        self.assertEqual(self.tree.size, 5)
        self.assertListEqual(_get_pre_order_tree(self.tree), [2, 1, 6, 4, 7])
        self.assertListEqual(_get_in_order_tree(self.tree), [1, 2, 4, 6, 7])
        self.assertListEqual(_get_post_order_tree(self.tree), [1, 4, 7, 6, 2])
        # right-left rotation
        self.tree.insert(3)
        self.assertEqual(self.tree.size, 6)
        self.assertListEqual(_get_pre_order_tree(self.tree), [4, 2, 1, 3, 6, 7])
        self.assertListEqual(_get_in_order_tree(self.tree), [1, 2, 3, 4, 6, 7])
        self.assertListEqual(_get_post_order_tree(self.tree), [1, 3, 2, 7, 6, 4])
        # left-right rotation
        self.tree.insert(-2)
        self.tree.insert(-1)
        self.assertEqual(self.tree.size, 8)
        self.assertListEqual(_get_pre_order_tree(self.tree), [4, 2, -1, -2, 1, 3, 6, 7])
        self.assertListEqual(_get_in_order_tree(self.tree), [-2, -1, 1, 2, 3, 4, 6, 7])
        self.assertListEqual(_get_post_order_tree(self.tree), [-2, 1, -1, 3, 2, 7, 6, 4.0])

    def test_contains(self) -> None:
        self.assertFalse(self.tree.contains(1))
        self.tree.insert(1)
        self.assertTrue(self.tree.contains(1))
        self.assertFalse(self.tree.contains(2))
        self.tree.insert(2)
        self.assertTrue(self.tree.contains(2))

    def test_find_max(self) -> None:
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_max)
        self.tree.insert(1)
        self.assertEqual(self.tree.find_max(), 1)
        self.tree.insert(3)
        self.assertEqual(self.tree.find_max(), 3)
        self.tree.insert(5)
        self.assertEqual(self.tree.find_max(), 5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        self.assertEqual(self.tree.find_max(), 5)

    def test_find_min(self) -> None:
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_min)
        self.tree.insert(1)
        self.assertEqual(self.tree.find_min(), 1)
        self.tree.insert(3)
        self.assertEqual(self.tree.find_min(), 1)
        self.tree.insert(5)
        self.assertEqual(self.tree.find_min(), 1)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        self.assertEqual(self.tree.find_min(), -1)

    def test_delete(self) -> None:
        self.tree.insert(1)
        self.tree.delete(1)
        self.assertEqual(self.tree.size, 0)
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        self.tree.delete(1)
        self.assertListEqual(_get_pre_order_tree(self.tree), [3, -1, 2, 5, 4])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2, 3, 4, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [2, -1, 4, 5, 3])
        self.tree.delete(3)
        self.assertListEqual(_get_pre_order_tree(self.tree), [2, -1, 5, 4])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2, 4, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [-1, 4, 5, 2])
        self.tree.delete(4)
        self.assertListEqual(_get_pre_order_tree(self.tree), [2, -1, 5])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2, 5])
        self.assertListEqual(_get_post_order_tree(self.tree), [-1, 5, 2])
        self.tree.delete(5)
        self.assertListEqual(_get_pre_order_tree(self.tree), [2, -1])
        self.assertListEqual(_get_in_order_tree(self.tree), [-1, 2])
        self.assertListEqual(_get_post_order_tree(self.tree), [-1, 2])
        self.tree.delete(-1)
        self.assertListEqual(_get_pre_order_tree(self.tree), [2])
        self.assertListEqual(_get_in_order_tree(self.tree), [2])
        self.assertListEqual(_get_post_order_tree(self.tree), [2])
        self.tree.delete(2)
        self.assertEqual(self.tree.size, 0)

    def test_clear(self) -> None:
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.clear()
        self.assertEqual(self.tree.size, 0)
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_max)
        self.assertRaises(OrderedBinaryTreeEmptyException, self.tree.find_min)

    def test_traverse(self) -> None:
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        pre_order: List[int] = []
        in_order: List[int] = []
        post_order: List[int] = []
        self.tree.traverse(lambda x: pre_order.append(x), TraversalType.PRE_ORDER)
        self.tree.traverse(lambda x: in_order.append(x), TraversalType.IN_ORDER)
        self.tree.traverse(lambda x: post_order.append(x), TraversalType.POST_ORDER)
        self.assertListEqual(pre_order, [3, 1, -1, 2, 5, 4])
        self.assertListEqual(in_order, [-1, 1, 2, 3, 4, 5])
        self.assertListEqual(post_order, [-1, 2, 1, 4, 5, 3])

    def test_generator(self) -> None:
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(5)
        self.tree.insert(-1)
        self.tree.insert(2)
        self.tree.insert(4)
        pre_order: List[int] = [*self.tree.generator(TraversalType.PRE_ORDER)]
        in_order: List[int] = [*self.tree.generator(TraversalType.IN_ORDER)]
        post_order: List[int] = [*self.tree.generator(TraversalType.POST_ORDER)]
        self.assertListEqual(pre_order, [3, 1, -1, 2, 5, 4])
        self.assertListEqual(in_order, [-1, 1, 2, 3, 4, 5])
        self.assertListEqual(post_order, [-1, 2, 1, 4, 5, 3])


class TreeStateSaveTest(unittest.TestCase):
    @dataclass
    @total_ordering
    class Item:
        value: int
        some_text: str = "default"

        def __lt__(self, other: TreeStateSaveTest.Item) -> bool:
            return self.value < other.value

        def __eq__(self, other: Any) -> bool:
            return isinstance(other, TreeStateSaveTest.Item) and self.value == other.value

    def tearDown(self) -> None:
        try:
            import os

            os.remove("search_tree.json")
            os.remove("avl_tree.json")
        except FileNotFoundError:
            pass

    def test_literal_in_search_tree(self) -> None:
        tree: IOrderedBinaryTree[int] = SearchTree()
        tree.insert(1)
        tree.insert(3)
        tree.insert(5)
        tree.insert(-1)
        tree.insert(2)
        tree.insert(4)
        OrderedBinaryTreeSerializer.save_tree_to_file(tree, "search_tree.json")
        tree.clear()
        OrderedBinaryTreeSerializer.load_tree_from_file(tree, "search_tree.json", int)
        self.assertListEqual(_get_pre_order_tree(tree), [1, -1, 3, 2, 5, 4])

    def test_item_in_search_tree(self) -> None:
        tree: IOrderedBinaryTree[TreeStateSaveTest.Item] = SearchTree()
        tree.insert(TreeStateSaveTest.Item(1))
        tree.insert(TreeStateSaveTest.Item(3))
        tree.insert(TreeStateSaveTest.Item(5))
        tree.insert(TreeStateSaveTest.Item(-1))
        tree.insert(TreeStateSaveTest.Item(2))
        tree.insert(TreeStateSaveTest.Item(4))
        OrderedBinaryTreeSerializer.save_tree_to_file(tree, "search_tree.json")
        tree.clear()
        OrderedBinaryTreeSerializer.load_tree_from_file(
            tree, "search_tree.json", TreeStateSaveTest.Item
        )
        self.assertListEqual(
            _get_pre_order_tree(tree),
            [
                TreeStateSaveTest.Item(1),
                TreeStateSaveTest.Item(-1),
                TreeStateSaveTest.Item(3),
                TreeStateSaveTest.Item(2),
                TreeStateSaveTest.Item(5),
                TreeStateSaveTest.Item(4),
            ],
        )

    def test_literal_in_avl_tree(self) -> None:
        tree: IOrderedBinaryTree[int] = AVLTree()
        tree.insert(1)
        tree.insert(3)
        tree.insert(5)
        tree.insert(-1)
        tree.insert(2)
        tree.insert(4)
        OrderedBinaryTreeSerializer.save_tree_to_file(tree, "avl_tree.json")
        tree.clear()
        OrderedBinaryTreeSerializer.load_tree_from_file(tree, "avl_tree.json", int)
        self.assertListEqual(_get_pre_order_tree(tree), [3, 1, -1, 2, 5, 4])

    def test_item_in_avl_tree(self) -> None:
        tree: IOrderedBinaryTree[TreeStateSaveTest.Item] = AVLTree()
        tree.insert(TreeStateSaveTest.Item(1))
        tree.insert(TreeStateSaveTest.Item(3))
        tree.insert(TreeStateSaveTest.Item(5))
        tree.insert(TreeStateSaveTest.Item(-1))
        tree.insert(TreeStateSaveTest.Item(2))
        tree.insert(TreeStateSaveTest.Item(4))
        OrderedBinaryTreeSerializer.save_tree_to_file(tree, "avl_tree.json")
        tree.clear()
        OrderedBinaryTreeSerializer.load_tree_from_file(
            tree, "avl_tree.json", TreeStateSaveTest.Item
        )
        self.assertListEqual(
            _get_pre_order_tree(tree),
            [
                TreeStateSaveTest.Item(3),
                TreeStateSaveTest.Item(1),
                TreeStateSaveTest.Item(-1),
                TreeStateSaveTest.Item(2),
                TreeStateSaveTest.Item(5),
                TreeStateSaveTest.Item(4),
            ],
        )


class TernaryTrieStrTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.trie: ITrie[str, int] = TernaryTrie()

    def test_get_or_none(self) -> None:
        self.assertIsNone(self.trie.get_or_none("apple"))
        self.trie.put("apple", 1)
        self.assertEqual(self.trie.get_or_none("apple"), 1)

    def test_get(self) -> None:
        self.assertRaises(TrieElementNotFound, self.trie.get, "apple")
        self.trie.put("apple", 1)
        self.assertEqual(self.trie.get("apple"), 1)

    def test_get_dunder(self) -> None:
        self.assertRaises(TrieElementNotFound, self.trie.__getitem__, "apple")
        self.trie.put("apple", 1)
        self.assertEqual(self.trie["apple"], 1)

    def test_contains(self) -> None:
        self.assertFalse(self.trie.contains("apple"))
        self.trie.put("apple", 1)
        self.assertTrue(self.trie.contains("apple"))

    def test_contains_dunder(self) -> None:
        self.assertFalse("apple" in self.trie)
        self.trie.put("apple", 1)
        self.assertTrue("apple" in self.trie)

    def test_delete(self) -> None:
        self.trie.put("apple", 1)
        self.trie.put("banana", 2)
        self.assertTrue(self.trie.contains("apple"))
        self.assertTrue(self.trie.delete("apple"))
        self.assertFalse(self.trie.contains("apple"))
        self.assertFalse(self.trie.delete("apple"))

    def test_clear(self) -> None:
        self.trie.put("apple", 1)
        self.trie.put("banana", 2)
        self.trie.clear()
        self.assertEqual(self.trie.size, 0)
        self.assertFalse(self.trie.contains("apple"))
        self.assertFalse(self.trie.contains("banana"))

    def test_size(self) -> None:
        self.assertEqual(self.trie.size, 0)
        self.trie.put("apple", 1)
        self.assertEqual(self.trie.size, 1)
        self.trie.put("banana", 2)
        self.assertEqual(self.trie.size, 2)
        self.trie.delete("banana")
        self.assertEqual(self.trie.size, 1)
        self.trie.put("app", 3)
        self.assertEqual(self.trie.size, 2)

    def test_keys_with_prefix(self) -> None:
        self.trie.put("apple", 1)
        self.trie.put("ape", 2)
        self.trie.put("bat", 3)
        self.trie.put("banana", 4)

        keys_with_ap_prefix: List[str] = list(self.trie.keys_with_prefix("ap"))
        self.assertListEqual(sorted(keys_with_ap_prefix), ["ape", "apple"])

        keys_with_b_prefix: List[str] = list(self.trie.keys_with_prefix("b"))
        self.assertListEqual(sorted(keys_with_b_prefix), ["banana", "bat"])

    def test_longest_prefix_of(self) -> None:
        self.trie.put("apple", 1)
        self.trie.put("ape", 2)
        self.trie.put("bat", 3)

        self.assertEqual(self.trie.longest_prefix_of("applejack"), "apple")
        self.assertEqual(self.trie.longest_prefix_of("apex"), "ape")
        self.assertEqual(self.trie.longest_prefix_of("batman"), "bat")
        self.assertIsNone(self.trie.longest_prefix_of("dog"))

    def test_merge(self) -> None:
        other_trie = TernaryTrie[str, int]()
        other_trie.put("dog", 1)
        other_trie.put("cat", 2)

        self.trie.put("apple", 1)
        self.trie.merge(other_trie)

        self.assertEqual(self.trie.get("apple"), 1)
        self.assertEqual(self.trie.get("dog"), 1)
        self.assertEqual(self.trie.get("cat"), 2)

    def test_is_empty(self) -> None:
        self.assertTrue(self.trie.is_empty())
        self.trie.put("apple", 1)
        self.assertFalse(self.trie.is_empty())

    def test_bool_dunder(self) -> None:
        self.assertFalse(self.trie)
        self.trie.put("apple", 1)
        self.assertTrue(self.trie)

    def test_len_dunder(self) -> None:
        self.assertEqual(len(self.trie), 0)
        self.trie.put("apple", 1)
        self.assertEqual(len(self.trie), 1)
        self.trie.put("banana", 2)
        self.assertEqual(len(self.trie), 2)
        self.trie.delete("banana")
        self.assertEqual(len(self.trie), 1)
        self.trie.put("app", 3)
        self.assertEqual(len(self.trie), 2)

    def test_traverse(self) -> None:
        self.trie.put("app", 1)
        self.trie.put("apple", 2)
        self.trie.put("ape", 3)
        self.trie.put("bat", 4)
        self.trie.put("ball", 5)

        pre_order_result: List[Tuple[str, int]] = []
        self.trie.traverse(lambda k, v: pre_order_result.append((k, v)), TraverseType.PRE_ORDER)
        self.assertListEqual(
            pre_order_result, [("app", 1), ("ape", 3), ("apple", 2), ("bat", 4), ("ball", 5)]
        )

        in_order_result: List[Tuple[str, int]] = []
        self.trie.traverse(lambda k, v: in_order_result.append((k, v)), TraverseType.IN_ORDER)
        self.assertListEqual(
            in_order_result, [("ape", 3), ("app", 1), ("apple", 2), ("ball", 5), ("bat", 4)]
        )

        post_order_result: List[Tuple[str, int]] = []
        self.trie.traverse(lambda k, v: post_order_result.append((k, v)), TraverseType.POST_ORDER)
        self.assertListEqual(
            post_order_result, [("ape", 3), ("apple", 2), ("app", 1), ("ball", 5), ("bat", 4)]
        )

    def test_generator(self) -> None:
        self.trie.put("app", 1)
        self.trie.put("apple", 2)
        self.trie.put("ape", 3)
        self.trie.put("bat", 4)
        self.trie.put("ball", 5)

        pre_order_generated: List[Tuple[str, int]] = list(
            self.trie.generator(TraverseType.PRE_ORDER)
        )
        self.assertListEqual(
            pre_order_generated, [("app", 1), ("ape", 3), ("apple", 2), ("bat", 4), ("ball", 5)]
        )

        in_order_generated: List[Tuple[str, int]] = list(self.trie.generator(TraverseType.IN_ORDER))
        self.assertListEqual(
            in_order_generated, [("ape", 3), ("app", 1), ("apple", 2), ("ball", 5), ("bat", 4)]
        )

        post_order_generated: List[Tuple[str, int]] = list(
            self.trie.generator(TraverseType.POST_ORDER)
        )
        self.assertListEqual(
            post_order_generated, [("ape", 3), ("apple", 2), ("app", 1), ("ball", 5), ("bat", 4)]
        )

    def test_str_dunder(self) -> None:
        self.trie.put("app", 1)
        self.trie.put("apple", 2)
        self.trie.put("ape", 3)
        self.trie.put("bat", 4)
        self.trie.put("ball", 5)

        self.assertEqual(
            str(self.trie),
            "TernaryTrie(ape: 3, app: 1, apple: 2, ball: 5, bat: 4)",
        )

        self.trie.clear()

        self.assertEqual(str(self.trie), "TernaryTrie()")


if __name__ == "__main__":
    unittest.main()
