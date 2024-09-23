from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from random import randint
from typing import Generator


@dataclass
@total_ordering
class Book:
    author: str
    publisher: str
    pages: int
    price: float
    isbn: str

    def __lt__(self, other: Book) -> bool:
        return (
            self.author < other.author
            or self.price < other.price
            or self.pages < other.pages
            or self.isbn < other.isbn
            or self.publisher < other.publisher
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Book)
            and self.author == other.author
            and self.publisher == other.publisher
            and self.pages == other.pages
            and self.price == other.price
            and self.isbn == other.isbn
        )

    def __str__(self) -> str:
        return f"Book(author: {self.author}, publisher: {self.publisher}, pages: {self.pages}, price: {self.price}, isbn: {self.isbn})"


def book_generator() -> Generator[Book]:
    while True:
        yield Book(
            f"Author {randint(1, 100)}",
            f"Publisher {randint(1, 100)}",
            randint(1, 1000),
            randint(1, 1000),
            f"ISBN {randint(1, 100)}",
        )
