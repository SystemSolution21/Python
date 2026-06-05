from typing import Any, TypeGuard


class APIError(Exception):
    """Custom error class with extra attributes for complex narrowing."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code: int = status_code


def assert_is_error(error: Any) -> None:
    """
    Equivalent to TypeScript's assertion function.
    In Python, we verify if the object is an instance of the base Exception class.
    """
    if not isinstance(error, Exception):
        raise TypeError(f"Expected an Exception, but got {type(error).__name__}")


def is_api_error(error: Any) -> TypeGuard[APIError]:
    """
    A TypeGuard function. If it returns True, the type checker narrows
    the type of 'error' to 'APIError' in that code path.
    """
    return isinstance(error, APIError) and hasattr(error, "status_code")


def divide(a: float, b: float) -> float:
    if b == 0:
        # Python's equivalent to 'throw new Error()'
        raise ValueError("Division by zero is not allowed.")
    return a / b


def main():
    try:
        result = divide(10, 0)
        print(f"Result: {result}")
    except Exception as error:
        # Narrowing the 'error' variable
        assert_is_error(error)

        # Complex narrowing using TypeGuard
        if is_api_error(error):
            # Type checkers now know 'error' is specifically an APIError
            # We can safely access 'status_code' with autocompletion
            print(f"Caught API Error ({error.status_code}): {error}")
        else:
            print(f"Caught {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
