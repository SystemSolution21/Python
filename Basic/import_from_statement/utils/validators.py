# Check Numbers
from typing import Any


def check_numbers(value: Any) -> bool:
    return isinstance(value, (int, float))
