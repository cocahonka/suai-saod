import unittest
from random import randint
from typing import Callable, List, Optional

from common.comparable import default_compare_to
from common.extra_typing import override
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList
from lab4.arrays.dynamic_array import DynamicArray
from lab5.algs.fibonacci_search import fibonacci_search
from lab5.algs.interpolation_search import interpolation_search
from lab5.type_aliases import SearchFunction, SearchSequence


class SearchTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.random_iteration: int = 1000
        self.random_size: int = 100
        self.random_upper: int = 50
        self.random_lower: int = -50

    def _get_random_sorted_list(
        self,
        size: int,
        upper_bound: Optional[int] = None,
        lower_bound: Optional[int] = None,
    ) -> List[int]:
        upper_bound = upper_bound or self.random_upper
        lower_bound = lower_bound or self.random_lower
        return sorted([randint(lower_bound, upper_bound) for _ in range(size)])

    def _get_expected_index(
        self,
        sequence: SearchSequence[int],
        target: int,
    ) -> List[int]:
        return (
            [-1] if target not in sequence else [i for i, x in enumerate(sequence) if x == target]
        )

    def _test_search(
        self,
        search_func: SearchFunction[int],
        sequence_transformer: Callable[[List[int]], SearchSequence[int]],
    ) -> None:
        standard_test_cases: List[List[int]] = [
            [],
            [1],
            [1, 2],
            [1, 1],
            [1, 2, 3],
            [1, 2, 3, 4],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
            [1, 6, 8, 8, 9, 17, 234, 234, 234, 812],
            [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1],
            [-10, -9, -8, -7, 5, 6, 7, 8, 9, 10],
        ]

        for test_case in standard_test_cases:
            sequence: SearchSequence[int] = sequence_transformer(test_case)
            for target in test_case + [-99, 99]:
                result: int = search_func(sequence, target, default_compare_to)
                self.assertIn(result, self._get_expected_index(test_case, target))

        for _ in range(self.random_iteration):
            sequence = sequence_transformer(self._get_random_sorted_list(self.random_size))
            target = randint(self.random_lower, self.random_upper)
            result = search_func(sequence, target, default_compare_to)
            self.assertIn(result, self._get_expected_index(sequence, target))

    def _convert_to_linked_list(self, array: List[int]) -> ILinkedList[int]:
        linked_list: ILinkedList[int] = DoublyLinkedList()
        [linked_list.add(x) for x in array]
        return linked_list

    def _convert_to_dynamic_array(self, array: List[int]) -> DynamicArray[int]:
        dynamic_array: DynamicArray[int] = DynamicArray()
        dynamic_array.add_all(array)
        return dynamic_array

    def test_fibonacci_search(self) -> None:
        self._test_search(fibonacci_search, list)
        self._test_search(fibonacci_search, self._convert_to_dynamic_array)
        self._test_search(fibonacci_search, self._convert_to_linked_list)

    def test_interpolation_search(self) -> None:
        self._test_search(interpolation_search, list)
        self._test_search(interpolation_search, self._convert_to_dynamic_array)
        self._test_search(interpolation_search, self._convert_to_linked_list)


if __name__ == "__main__":
    unittest.main()
