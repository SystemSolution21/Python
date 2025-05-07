# Binary Search
"""
This module implements the binary search algorithm.

Binary search is an efficient algorithm for finding an item from a sorted
list of items. It works by repeatedly dividing in half the portion of the
list that could contain the item, until you've narrowed down the
possible locations to just one.
"""


def binary_search(array: list[int], target: int) -> int:
    """
    Performs a binary search on a sorted list of integers.

    Args:
        array: A sorted list of integers to search within.
        target: The integer value to search for.
    Returns:
        The index of the target in the array if found, otherwise -1.
    """
    low: int = 0
    high: int = len(array) - 1

    while low <= high:
        mid: int = (low + high) // 2

        if array[mid] == target:
            return mid  # target found at index mid

        elif array[mid] < target:
            low = mid + 1  # search high side

        else:
            high = mid - 1  # search low side

    return -1


# Usage
array: list[int] = [1, 3, 5, 7, 9, 11, 13, 15]
target: int = 7

result: int = binary_search(array=array, target=target)

if result != -1:
    print(f"Target {target} found at index {result}")
else:
    print(f"Target {target} not found in the array")
