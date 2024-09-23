from itertools import islice as take
from typing import Callable, Dict

from lab4.algs.arrays.insertion_sort import insertion_sort
from lab4.arrays.array import IArray
from lab4.arrays.dynamic_array import DynamicArray
from lab4.models.book import Book, book_generator


def insertion_sort_example() -> None:
    end: str = "\n\n"

    books: IArray[Book] = DynamicArray()
    books.add_all([*take(book_generator(), 10)])

    print("Before sorting:")
    for book in books:
        print(book)
    print(end)

    insertion_sort(books, lambda a, b: a.price < b.price)
    print("After sorting (by ascending price):")
    for book in books:
        print(book)
    print(end)


def main() -> None:
    functions: Dict[str, Callable[..., object]] = {
        "Insertion sort": insertion_sort_example,
    }

    pfix: str = "=" * 20
    for name, function in functions.items():
        print(f"{pfix} {name} {pfix}")
        function()
        print("\n\n")


if __name__ == "__main__":
    main()
