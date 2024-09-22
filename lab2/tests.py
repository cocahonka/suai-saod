from __future__ import annotations

import unittest
from typing import Any

from common.extra_typing import override
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList
from lab2.main import is_valid_braces_sequence
from lab2.stack.not_growable_stack import NotGrowableStack
from lab2.stack.stack import IStack, StackEmptyException, StackOverflowException
from lab2.stack.stack_linked_list import StackLinkedList


class LinkedListTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.linked_list: ILinkedList[Any] = DoublyLinkedList()

    def test_add(self) -> None:
        self.linked_list.add(1)
        self.assertEqual(len(self.linked_list), 1)
        self.assertEqual(self.linked_list[0], 1)

    def test_add_in_head(self) -> None:
        self.linked_list.add_in_head(1)
        self.linked_list.add_in_head(2)
        self.assertEqual(self.linked_list[0], 2)

    def test_add_in_tail(self) -> None:
        self.linked_list.add_in_tail(1)
        self.linked_list.add_in_tail(2)
        self.assertEqual(self.linked_list[0], 1)

    def test_insert(self) -> None:
        self.linked_list.add(1)
        self.linked_list.add(3)
        self.linked_list.insert(1, 2)
        self.assertEqual(self.linked_list[1], 2)
        with self.assertRaises(IndexError):
            self.linked_list.insert(4, 4)

    def test_element_at(self) -> None:
        self.linked_list.add(1)
        self.linked_list.add(2)
        self.assertEqual(self.linked_list.element_at(1), 2)
        with self.assertRaises(IndexError):
            self.linked_list.element_at(2)

    def test_element_at_or_none(self) -> None:
        self.linked_list.add(1)
        self.assertEqual(self.linked_list.element_at_or_none(0), 1)
        self.assertIsNone(self.linked_list.element_at_or_none(1))

    def test_get_item_dunder(self) -> None:
        self.linked_list.add(1)
        self.assertEqual(self.linked_list[0], 1)
        with self.assertRaises(IndexError):
            self.linked_list[1]

    def test_contains(self) -> None:
        self.linked_list.add(1)
        self.assertTrue(self.linked_list.contains(1))
        self.assertFalse(self.linked_list.contains(2))

    def test_contains_dunder(self) -> None:
        self.linked_list.add(1)
        self.assertTrue(1 in self.linked_list)
        self.assertFalse(2 in self.linked_list)

    def test_update(self) -> None:
        self.linked_list.add(1)
        self.linked_list.update(0, 2)
        self.assertEqual(self.linked_list[0], 2)
        with self.assertRaises(IndexError):
            self.linked_list.update(1, 2)

    def test_set_item_dunder(self) -> None:
        self.linked_list.add(1)
        self.linked_list[0] = 2
        self.assertEqual(self.linked_list[0], 2)

    def test_clear(self) -> None:
        self.linked_list.add(1)
        self.linked_list.clear()
        self.assertEqual(len(self.linked_list), 0)

    def test_remove(self) -> None:
        self.linked_list.add(1)
        self.assertTrue(self.linked_list.remove(1))
        self.assertFalse(self.linked_list.remove(1))

    def test_remove_at(self) -> None:
        self.linked_list.add(1)
        self.linked_list.remove_at(0)
        self.assertEqual(len(self.linked_list), 0)
        with self.assertRaises(IndexError):
            self.linked_list.remove_at(0)

    def test_del_item_dunder(self) -> None:
        self.linked_list.add(1)
        del self.linked_list[0]
        self.assertEqual(len(self.linked_list), 0)
        with self.assertRaises(IndexError):
            del self.linked_list[0]

    def test_is_empty(self) -> None:
        self.assertTrue(self.linked_list.is_empty())
        self.linked_list.add(1)
        self.assertFalse(self.linked_list.is_empty())

    def test_bool_dunder(self) -> None:
        self.assertFalse(self.linked_list)
        self.linked_list.add(1)
        self.assertTrue(self.linked_list)

    def test_len_dunder(self) -> None:
        self.assertEqual(len(self.linked_list), 0)
        self.linked_list.add(1)
        self.assertEqual(len(self.linked_list), 1)

    def test_str_dunder(self) -> None:
        self.assertEqual(str(self.linked_list), "[]")
        self.linked_list.add(1)
        self.assertEqual(str(self.linked_list), "[1]")
        self.linked_list.add(2)
        self.assertEqual(str(self.linked_list), "[1 -> 2]")

    def test_iteration(self) -> None:
        self.linked_list.add(1)
        self.linked_list.add(2)
        self.linked_list.add(3)
        for i, value in enumerate(self.linked_list):
            self.assertEqual(value, i + 1)

    def test_reversed_dunder(self) -> None:
        self.linked_list.add(1)
        self.linked_list.add(2)
        self.linked_list.add(3)
        for i, value in enumerate(reversed(self.linked_list)):
            self.assertEqual(value, 3 - i)

    def test_reverse(self) -> None:
        self.linked_list.add(1)
        self.linked_list.add(2)
        self.linked_list.add(3)
        self.linked_list.reverse()
        for i, value in enumerate(self.linked_list):
            self.assertEqual(value, 3 - i)


class StackTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.stack: IStack[Any] = StackLinkedList()

    def test_push(self) -> None:
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(len(self.stack), 2)
        self.assertEqual(self.stack.peek(), 2)

    def test_not_growable_push(self) -> None:
        stack: IStack[Any] = NotGrowableStack(self.stack, 1)
        stack.push(1)
        with self.assertRaises(StackOverflowException):
            stack.push(2)

    def test_peek(self) -> None:
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.peek(), 2)
        self.assertEqual(len(self.stack), 2)
        self.stack.pop()
        self.stack.pop()
        with self.assertRaises(StackEmptyException):
            self.stack.peek()

    def test_peek_or_none(self) -> None:
        self.assertIsNone(self.stack.peek_or_none())
        self.stack.push(1)
        self.assertEqual(self.stack.peek_or_none(), 1)

    def test_pop(self) -> None:
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(len(self.stack), 1)
        self.stack.pop()
        with self.assertRaises(StackEmptyException):
            self.stack.pop()

    def test_pop_or_none(self) -> None:
        self.assertIsNone(self.stack.pop_or_none())
        self.stack.push(1)
        self.assertEqual(self.stack.pop_or_none(), 1)

    def test_clear(self) -> None:
        self.stack.push(1)
        self.stack.push(2)
        self.stack.clear()
        self.assertEqual(len(self.stack), 0)

    def test_is_empty(self) -> None:
        self.assertTrue(self.stack.is_empty())
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())

    def test_bool_dunder(self) -> None:
        self.assertFalse(self.stack)
        self.stack.push(1)
        self.assertTrue(self.stack)

    def test_capacity(self) -> None:
        self.assertEqual(self.stack.capacity, 0)
        self.stack.push(1)
        self.assertEqual(self.stack.capacity, 1)

    def test_not_growable_capacity(self) -> None:
        stack: IStack[Any] = NotGrowableStack(self.stack, 2)
        self.assertEqual(stack.capacity, 2)

    def test_len_dunder(self) -> None:
        self.assertEqual(len(self.stack), 0)
        self.stack.push(1)
        self.assertEqual(len(self.stack), 1)


class BracesTest(unittest.TestCase):
    def test_is_valid_braces_sequence(self) -> None:
        self.assertTrue(is_valid_braces_sequence("()"))
        self.assertTrue(is_valid_braces_sequence("()[]{}"))
        self.assertTrue(is_valid_braces_sequence("{[]}"))
        self.assertFalse(is_valid_braces_sequence("(]"))
        self.assertFalse(is_valid_braces_sequence("([)]"))
        self.assertFalse(is_valid_braces_sequence("]"))
        self.assertFalse(is_valid_braces_sequence("["))
        self.assertFalse(is_valid_braces_sequence("()[]{}("))
        self.assertTrue(is_valid_braces_sequence("([{()[]{}}])"))


if __name__ == "__main__":
    unittest.main()
