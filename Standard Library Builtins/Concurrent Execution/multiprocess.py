# multiprocessing.ipynb
# multiprocessing is a package that supports spawning processes using an API similar to the threading module.
# multiprocessing.Pool() - A pool of workers processes
# multiprocessing.Process() - A single worker process
# multiprocessing.Queue() - A queue for passing messages to worker processes
# multiprocessing.Lock() - A lock for synchronizing access to shared resources
# multiprocessing.Value() - A wrapper for a single shared value
# multiprocessing.Array() - A wrapper for a shared array

import os
import time
from functools import wraps
from multiprocessing import Pool
from typing import Any, Callable


# Execution time decorator
def execution_time(func: Callable[..., list[int]]) -> Callable[..., list[int]]:
    """Measure the execution time of a function."""

    @wraps(wrapped=func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"Start timing {func.__name__}...")
        start: float = time.perf_counter()
        result = func(*args, **kwargs)
        end: float = time.perf_counter()
        execution_time: float = end - start
        print(f"Execution time of {func.__name__}: {execution_time:.3f} seconds")
        return result

    return wrapper


# Compute Task
def compute_task(num: int) -> int:
    """Compute a task."""
    for _ in range(100_000):
        num *= 2
    return num


# Single Process
@execution_time
def single_process_compute(num_list: list[int]) -> list[int]:
    return [compute_task(num) for num in num_list]


# Multi Process
@execution_time
def multi_process_compute(num_list: list[int]) -> list[int]:
    with Pool() as pool:
        return pool.map(compute_task, num_list)


# Main Entry
def main() -> None:
    print(f"Number of CPU: {os.cpu_count()}")
    num_list: list[int] = list(range(1, 100))
    try:
        assert single_process_compute(num_list) == multi_process_compute(num_list)
        print("Assertion passed! Computation result is the same.")
    except AssertionError:
        print("Assertion failed! Computation result is not the same.")


if __name__ == "__main__":
    main()
