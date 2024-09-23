from __future__ import annotations

import unittest
from random import randint
from typing import Callable, Generator, List

from common.extra_typing import override
from lab4.algs.arrays.insertion_sort import insertion_sort
from lab4.arrays.array import (
    ArrayIndexOutOfBoundsException,
    ArrayOverflowException,
    IArray,
)
from lab4.arrays.dynamic_array import DynamicArray
from lab4.arrays.not_growable_array import NotGrowableArray


class ArrayTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.array: IArray[int] = DynamicArray(1)

    def test_add(self) -> None:
        self.array.add(1)
        self.assertEqual(len(self.array), 1)
        self.assertEqual(self.array[0], 1)

    def test_not_growable_add(self) -> None:
        array: IArray[int] = NotGrowableArray(self.array, 1)
        array.add(1)
        with self.assertRaises(ArrayOverflowException):
            array.add(2)

    def test_add_all(self) -> None:
        self.array.add_all([1, 2])
        self.assertEqual(len(self.array), 2)
        self.assertEqual(self.array[0], 1)
        self.assertEqual(self.array[1], 2)

        self.array.add_all(self.array[::])
        self.assertEqual(len(self.array), 4)
        self.assertEqual(self.array[0], 1)
        self.assertEqual(self.array[1], 2)
        self.assertEqual(self.array[2], 1)
        self.assertEqual(self.array[3], 2)

    def test_not_growable_add_all(self) -> None:
        array: IArray[int] = NotGrowableArray(self.array, 3)
        array.add_all([1, 2])
        with self.assertRaises(ArrayOverflowException):
            array.add_all([3, 4])

    def test_insert(self) -> None:
        self.array.add(1)
        self.array.add(3)
        self.array.insert(1, 2)
        self.assertEqual(self.array[0], 1)
        self.assertEqual(self.array[1], 2)
        self.assertEqual(self.array[2], 3)
        with self.assertRaises(ArrayIndexOutOfBoundsException):
            self.array.insert(4, 4)

    def test_not_growable_insert(self) -> None:
        array: IArray[int] = NotGrowableArray(self.array, 3)
        array.add(1)
        array.add(3)
        array.insert(1, 2)
        with self.assertRaises(ArrayOverflowException):
            array.insert(2, 4)

    def test_element_at(self) -> None:
        self.array.add(1)
        self.array.add(2)
        self.assertEqual(self.array.element_at(1), 2)
        with self.assertRaises(ArrayIndexOutOfBoundsException):
            self.array.element_at(2)

    def test_element_at_or_none(self) -> None:
        self.array.add(1)
        self.assertEqual(self.array.element_at_or_none(0), 1)
        self.assertIsNone(self.array.element_at_or_none(1))

    def test_get_item_dunder(self) -> None:
        self.array.add(1)
        self.assertEqual(self.array[0], 1)
        self.assertEqual(self.array[-1], 1)
        with self.assertRaises(ArrayIndexOutOfBoundsException):
            self.array[1]

    def test_get_item_dunder_slice(self) -> None:
        self.array.add_all([1, 2, 3, 4])
        self.assertEqual([x for x in self.array[1:3]], [2, 3])
        self.assertEqual([x for x in self.array[1:]], [2, 3, 4])
        self.assertEqual([x for x in self.array[:3]], [1, 2, 3])
        self.assertEqual([x for x in self.array[:]], [1, 2, 3, 4])
        self.assertEqual([x for x in self.array[1:3:2]], [2])
        self.assertEqual([x for x in self.array[::-1]], [4, 3, 2, 1])

    def test_index_of(self) -> None:
        self.array.add(1)
        self.array.add(2)
        self.assertEqual(self.array.index_of(1), 0)
        self.assertEqual(self.array.index_of(2), 1)
        self.assertEqual(self.array.index_of(3), -1)

    def test_len(self) -> None:
        self.array.add(1)
        self.assertEqual(len(self.array), 1)
        self.array.add(2)
        self.assertEqual(len(self.array), 2)
        self.array.remove_at(0)
        self.assertEqual(len(self.array), 1)

    def test_contains(self) -> None:
        self.array.add(1)
        self.assertTrue(self.array.contains(1))
        self.assertFalse(self.array.contains(2))

    def test_contains_dunder(self) -> None:
        self.array.add(1)
        self.assertTrue(1 in self.array)
        self.assertFalse(2 in self.array)

    def test_update(self) -> None:
        self.array.add(1)
        self.array.update(0, 2)
        self.assertEqual(self.array[0], 2)
        with self.assertRaises(ArrayIndexOutOfBoundsException):
            self.array.update(1, 2)

    def test_set_item_dunder(self) -> None:
        self.array.add(1)
        self.array[0] = 2
        self.assertEqual(self.array[0], 2)
        with self.assertRaises(ArrayIndexOutOfBoundsException):
            self.array[1] = 2

    def test_remove(self) -> None:
        self.array.add(1)
        self.assertTrue(self.array.remove(1))
        self.assertFalse(self.array.remove(1))

    def test_remove_at(self) -> None:
        self.array.add(1)
        self.assertEqual(self.array.remove_at(0), 1)
        with self.assertRaises(ArrayIndexOutOfBoundsException):
            self.array.remove_at(0)

    def test_clear(self) -> None:
        self.array.add(1)
        self.array.clear()
        self.assertEqual(len(self.array), 0)

    def test_reverse(self) -> None:
        self.array.add_all([1, 2, 3, 4])
        self.assertEqual([*reversed(self.array)], [4, 3, 2, 1])


class SortingTest(unittest.TestCase):
    def random_list_generator(
        self,
        size: int,
        upper_bound: int = 100_000,
        lower_bound: int = -100_000,
    ) -> Generator[List[int]]:
        while True:
            yield [randint(lower_bound, upper_bound) for _ in range(size)]

    def _test_sorting(self, sort_func: Callable[[List[int]], None]) -> None:
        test_cases: List[List[int]] = [
            [],
            [5],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [3, 1, 4, 3, 2],
            [-3, -1, 4, 2, 0],
        ]

        for case in test_cases:
            array: List[int] = case.copy()
            sort_func(array)
            self.assertListEqual(array, sorted(case))

        for _ in range(100):
            array = next(self.random_list_generator(100))
            sort_func(array)
            self.assertListEqual(array, sorted(array))

    def test_insertion_sort(self) -> None:
        self._test_sorting(insertion_sort)


if __name__ == "__main__":
    unittest.main()
