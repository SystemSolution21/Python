from functools import wraps
from typing import Any, Callable


def decorator1(func) -> Callable[..., Any]:
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"{decorator1.__name__}: call before {func.__name__} execution")
        result: Any = func(*args, **kwargs)
        print(f"{decorator1.__name__}: call after {func.__name__} execution")
        return result

    return wrapper


def decorator2(func) -> Callable[..., Any]:
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"{decorator2.__name__}: call before {func.__name__} execution")
        result: Any = func(*args, **kwargs)
        print(f"{decorator2.__name__}: call after {func.__name__} execution")
        return result

    return wrapper


# Multiple Decorators
@decorator1
@decorator2
def my_function() -> None:
    print(f"Executing {my_function.__name__}.....")


# Usage
def main() -> None:
    my_function()


if __name__ == "__main__":
    main()
