from __future__ import annotations

from dataclasses import dataclass
from typing import Union, overload

from common.comparable import Comparable


@dataclass
class Number:
    value: int

    def __len__(self) -> int:
        return len(str(self.value))

    @overload
    def __getitem__(self, index: int) -> Comparable: ...

    @overload
    def __getitem__(self, slice: slice) -> Number: ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Comparable, Number]:
        if isinstance(index, int):
            return int(str(self.value)[index])
        return Number(int(str(self.value)[index]))

    def __repr__(self) -> str:
        return f"Number({self.value})"
