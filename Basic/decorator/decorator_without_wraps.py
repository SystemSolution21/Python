# Decorator without wraps
"""
Without wraps, the metadata of the original function is lost.
"""

# from functools import wraps
from typing import Any, Callable


def my_decorator(func) -> Callable[..., Any]:
    # @wraps(wrapped=func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    return wrapper


@my_decorator
def original_function() -> None:
    """This is the original function."""

    print("Original function called.")


def main() -> None:
    original_function()
    print(f"{original_function.__name__ = }")  # Output: "wrapper"
    print(f"{original_function.__doc__ = }")  # Output: None


if __name__ == "__main__":
    main()
