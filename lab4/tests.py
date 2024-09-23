import unittest

from common.extra_typing import override
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


if __name__ == "__main__":
    unittest.main()
