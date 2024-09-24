from __future__ import annotations

import inspect
import timeit
from abc import ABC
from typing import Any, Callable, List, Optional, Tuple, Union, get_type_hints

VoidCallback = Callable[[], None]
BenchmarkCallback = Union[Tuple[VoidCallback, int], Tuple[VoidCallback, int, int]]
BenchmarkMethod = Callable[["Benchmark"], BenchmarkCallback]


class Benchmark(ABC):
    @classmethod
    def run_benchmarks(cls) -> None:
        benchmark_methods: List[BenchmarkMethod] = cls._get_benchmark_methods()

        for method in benchmark_methods:
            instance: Benchmark = cls()
            instance.setUp()

            result: BenchmarkCallback = method(instance)
            callback: VoidCallback
            iterations: int
            count_of_elements: Optional[int] = None

            if len(result) == 2:
                callback, iterations = result
            else:
                callback, iterations, count_of_elements = result

            postfix: str = f" and {count_of_elements} elements" if count_of_elements else ""
            print(
                f"Running {cls.__name__}.{method.__name__} with {iterations} iterations{postfix}..."
            )
            time_taken = timeit.timeit(callback, number=iterations)
            print(
                f"Completed {iterations} iterations in {time_taken:.6f} seconds",
                end="\n\n",
            )

            instance.tearDown()

    @classmethod
    def _get_benchmark_methods(cls) -> List[BenchmarkMethod]:
        methods: List[BenchmarkMethod] = []

        for method_name in dir(cls):
            if not method_name.startswith("benchmark_"):
                continue

            method: Any = getattr(cls, method_name)
            if callable(method) and get_type_hints(method).get("return", None) == BenchmarkCallback:
                methods.append(method)

        return methods

    def setUp(self) -> None: ...

    def tearDown(self) -> None: ...


def main() -> None:
    module = __import__("__main__")
    for name, obj in module.__dict__.items():
        if inspect.isclass(obj) and issubclass(obj, Benchmark) and obj is not Benchmark:
            obj.run_benchmarks()
