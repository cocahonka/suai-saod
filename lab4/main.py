from itertools import islice as take
from typing import Callable, Dict

from lab2.linked_list.doubly_linked_list import DoublyLinkedList
from lab2.linked_list.linked_list import ILinkedList
from lab4.algs.arrays.insertion_sort import insertion_sort
from lab4.algs.arrays.merge_sort import merge_sort, merge_sort_in_place
from lab4.algs.linked_list.counting_sort import counting_sort_through_public_api
from lab4.algs.linked_list.gnome_sort import gnome_sort_through_public_api
from lab4.arrays.array import IArray
from lab4.arrays.dynamic_array import DynamicArray
from lab4.models.book import Book, book_generator

Comparator = Callable[[Book, Book], bool]
IntKeySelector = Callable[[Book], int]

ArraySortFunction = Callable[[IArray[Book], Comparator], None]
LinkedListSortFunction = Callable[[ILinkedList[Book], Comparator], None]
LinkedListSortByKeyFunction = Callable[[ILinkedList[Book], IntKeySelector], None]


def array_sort_example(
    sort_function: ArraySortFunction,
    comparator: Comparator,
    criteria: str,
) -> None:
    books: IArray[Book] = DynamicArray()
    books.add_all([*take(book_generator(), 10)])

    print("Before sorting:")
    for book in books:
        print(book)
    print()

    sort_function(books, comparator)
    print(f"After sorting (by {criteria}):")
    for book in books:
        print(book)


def linked_list_sort_example(
    sort_function: LinkedListSortFunction,
    comparator: Comparator,
    criteria: str,
) -> None:
    books: ILinkedList[Book] = DoublyLinkedList()
    [books.add(book) for book in take(book_generator(), 10)]

    print("Before sorting:")
    for book in books:
        print(book)
    print()

    sort_function(books, comparator)
    print(f"After sorting (by {criteria}):")
    for book in books:
        print(book)


def linked_list_sort_example_by_key(
    sort_function: LinkedListSortByKeyFunction,
    key_selector: IntKeySelector,
    criteria: str,
    ascending: bool = False,
) -> None:
    books: ILinkedList[Book] = DoublyLinkedList()
    [books.add(book) for book in take(book_generator(), 10)]

    print("Before sorting:")
    for book in books:
        print(book)
    print()

    sort_function(books, key_selector)

    print(f"After sorting (by {criteria}):")

    if not ascending:
        books.reverse()

    for book in books:
        print(book)


def main() -> None:
    functions: Dict[str, Callable[..., object]] = {
        "Insertion sort": lambda: array_sort_example(
            insertion_sort,
            lambda a, b: a.price < b.price,
            "ascending price",
        ),
        "Merge sort": lambda: array_sort_example(
            merge_sort,
            lambda a, b: a.author > b.author,
            "descending author",
        ),
        "Merge sort (in-place)": lambda: array_sort_example(
            merge_sort_in_place,
            lambda a, b: a.author > b.author,
            "descending author",
        ),
        "Gnome sort (public API)": lambda: linked_list_sort_example(
            gnome_sort_through_public_api,
            lambda a, b: a.author < b.author,
            "ascending author",
        ),
        "Counting sort (public API)": lambda: linked_list_sort_example_by_key(
            counting_sort_through_public_api,
            lambda a: a.pages,
            "descending pages",
            ascending=False,
        ),
    }

    pfix: str = "=" * 20

    for name, function in functions.items():
        print(f"{pfix} {name} {pfix}")
        function()
        print(end="\n\n")


if __name__ == "__main__":
    main()
