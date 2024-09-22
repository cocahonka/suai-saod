from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering


@dataclass
@total_ordering
class Student:
    full_name: str
    group_number: str
    course: int
    age: int
    average_grade: float

    def __lt__(self, other: Student) -> bool:
        return self.average_grade < other.average_grade

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Student) and self.average_grade == other.average_grade

    def __str__(self) -> str:
        return f"{self.full_name} id({id(self)}) avg({self.average_grade})"
