import sys
import sysconfig
import math
import time
import threading
import multiprocessing


# Execution time decorator
def timeit(func):
    def wrapper(*args, **kwargs):
        start_time: float = time.time()
        result = func(*args, **kwargs)
        end_time: float = time.time()
        execution_time: float = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time:.3f} seconds")
        return result

    return wrapper


# Compute Factorial
def compute_factorial(n):
    return math.factorial(n)


# Single Threaded
@timeit
def single_threaded_compute(num_list: list[int]):
    for num in num_list:
        compute_factorial(num)

    print("single threaded compute done.")


# Multi Threaded
@timeit
def multi_threaded_compute(num_list: list[int]):
    threads: list[threading.Thread] = []

    # Create threads
    for num in num_list:
        thread = threading.Thread(target=compute_factorial, args=(num,))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for the threads to finish
    for thread in threads:
        thread.join()

    print(f"multi threaded compute done.")


# Multi Processing
@timeit
def multi_processing_compute(num_list: list[int]):
    processes: list[multiprocessing.Process] = []

    # Create processes
    for num in num_list:
        process = multiprocessing.Process(target=compute_factorial, args=(num,))
        processes.append(process)

    # Start the processes
    for process in processes:
        process.start()

    # Wait for the processes to finish
    for process in processes:
        process.join()

    print("multi processing compute done.")


# Main
def main() -> None:
    # Python Version
    print(f"python version: {sys.version}")

    # GIL Status
    gil_status = sysconfig.get_config_var(name="Py_GIL_DISABLED")

    if gil_status is None:
        print("gil cannot be disabled")
    elif gil_status == 0:
        print("gil is active")
    elif gil_status == 1:
        print("gil is disabled")

    # List of Numbers
    num_list: list[int] = [100_000, 200_000, 300_000, 400_000, 500_000]

    # Execute Single Thread
    single_threaded_compute(num_list=num_list)

    # Execute Multi Thread
    multi_threaded_compute(num_list=num_list)

    # Execute Multi Process
    multi_processing_compute(num_list=num_list)


if __name__ == "__main__":

    main()
