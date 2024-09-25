from __future__ import annotations

from common.comparable import default_compare_to
from lab5.main import C, Comparator, KeySelector, SearchSequence, T


def interpolation_search(
    sequence: SearchSequence[C],
    target: C,
    compare: Comparator[C] = default_compare_to,
) -> int:
    return interpolation_search_by(
        sequence,
        target,
        lambda x: x,
        compare,
    )


def interpolation_search_by(
    sequence: SearchSequence[T],
    target: C,
    key_selector: KeySelector[T, C],
    compare: Comparator[C] = default_compare_to,
) -> int:
    raise NotImplemented
