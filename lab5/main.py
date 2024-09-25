from __future__ import annotations

from itertools import islice as take
from random import choice
from typing import Callable, Dict

from common.comparable import default_compare_to
from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList
from lab4.algs.arrays.insertion_sort import insertion_sort
from lab4.algs.arrays.merge_sort import merge_sort
from lab4.algs.linked_list.gnome_sort import gnome_sort_through_public_api
from lab4.arrays.array import IArray
from lab4.arrays.dynamic_array import DynamicArray
from lab4.main import ArraySortFunction
from lab4.main import Comparator as SortComparator
from lab4.main import LinkedListSortFunction
from lab4.models.book import Book, book_generator
from lab5.algs.fibonacci_search import fibonacci_search_by
from lab5.type_aliases import C, SearchByFunction, SearchComparator, SearchKeySelector


def array_search_example(
    sort_function: ArraySortFunction,
    sort_comparator: SortComparator,
    sort_criteria: str,
    search_function: SearchByFunction[Book, C],
    search_comparator: SearchComparator[C],
    search_selector: SearchKeySelector[Book, C],
    search_criteria: str,
) -> None:
    books: IArray[Book] = DynamicArray()
    books.add_all([*take(book_generator(), 10)])

    print("Before sorting:")
    for i, book in enumerate(books):
        print(i, book)
    print()

    sort_function(books, sort_comparator)
    print(f"After sorting (by {sort_criteria}):")
    for i, book in enumerate(books):
        print(i, book)
    print()

    book = choice(books)
    target: C = search_selector(book)
    print(f"Searching book by {search_criteria} ({target}):")
    index: int = search_function(books, target, search_selector, search_comparator)
    print(f"Found at index: {index}" if index != -1 else "Not found")


def linked_list_search_example(
    sort_function: LinkedListSortFunction,
    sort_comparator: SortComparator,
    sort_criteria: str,
    search_function: SearchByFunction[Book, C],
    search_comparator: SearchComparator[C],
    search_selector: SearchKeySelector[Book, C],
    search_criteria: str,
) -> None:
    books: ILinkedList[Book] = DoublyLinkedList()
    [books.add(book) for book in take(book_generator(), 10)]

    print("Before sorting:")
    for i, book in enumerate(books):
        print(i, book)
    print()

    sort_function(books, sort_comparator)
    print(f"After sorting (by {sort_criteria}):")
    for i, book in enumerate(books):
        print(i, book)
    print()

    book = choice(books)
    target: C = search_selector(book)
    print(f"Searching book by {search_criteria} ({target}):")
    index: int = search_function(books, target, search_selector, search_comparator)
    print(f"Found at index: {index}" if index != -1 else "Not found")


def main() -> None:
    functions: Dict[str, Callable[..., object]] = {
        "Fibonacci search in array": lambda: array_search_example(
            sort_function=insertion_sort,
            sort_comparator=lambda a, b: a.pages < b.pages,
            sort_criteria="ascending page count",
            search_function=fibonacci_search_by,
            search_comparator=default_compare_to,
            search_selector=lambda book: book.pages,
            search_criteria="page count",
        ),
        "Fibonacci search in linked list": lambda: linked_list_search_example(
            sort_function=gnome_sort_through_public_api,
            sort_comparator=lambda a, b: a.pages < b.pages,
            sort_criteria="ascending page count",
            search_function=fibonacci_search_by,
            search_comparator=default_compare_to,
            search_selector=lambda book: book.pages,
            search_criteria="page count",
        ),
        "Interpolation search in array": lambda: array_search_example(
            sort_function=merge_sort,
            sort_comparator=lambda a, b: a.pages < b.pages,
            sort_criteria="ascending page count",
            search_function=fibonacci_search_by,
            search_comparator=default_compare_to,
            search_selector=lambda book: book.pages,
            search_criteria="page count",
        ),
        "Interpolation search in linked list": lambda: linked_list_search_example(
            sort_function=gnome_sort_through_public_api,
            sort_comparator=lambda a, b: a.pages < b.pages,
            sort_criteria="ascending page count",
            search_function=fibonacci_search_by,
            search_comparator=default_compare_to,
            search_selector=lambda book: book.pages,
            search_criteria="page count",
        ),
    }

    pfix: str = "=" * 20

    for name, function in functions.items():
        print(f"{pfix} {name} {pfix}")
        function()
        print(end="\n\n")

    # Mini Showcase for flexibility
    some_list: DynamicArray[Book] = DynamicArray()
    some_list.add_all(
        [
            Book("Aron", "B", 1, 1.2, "1234"),
            Book("Bill", "C", 2, 2.3, "2345"),
            Book("Zon", "D", 3, 3.4, "3456"),
            Book("Allay", "E", 4, 4.5, "4567"),
        ]
    )
    print("Before sorting:")
    for i, book in enumerate(some_list):
        print(i, book)

    merge_sort(some_list, lambda a, b: a.author > b.author)

    print("Sorted by descending author:")
    for i, book in enumerate(some_list):
        print(i, book)

    print("Searching for book with 'Ar' author:")
    index: int = fibonacci_search_by(
        some_list, "Ar", lambda book: book.author[:2], lambda a, b: default_compare_to(b, a)
    )
    print(f"Found at index: {index}")


if __name__ == "__main__":
    main()
