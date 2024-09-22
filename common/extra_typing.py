import sys
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])

if sys.version_info >= (3, 12):
    from typing import Self, override
else:

    def override(method: F) -> F:
        return method

    Self = Any


def contravariant_args(method: F) -> F:
    """https://github.com/python/typing/issues/548"""
    return method


__all__ = ["override", "Self", "contravariant_args"]
