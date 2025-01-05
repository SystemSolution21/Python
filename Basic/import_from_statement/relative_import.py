import sys
from .helpers import math_operations
from .utils import validators


# Use "python -m import_from_statement.relative_import" to run this script
def main() -> None:

    print(sys.path[0])

    result: int | float = math_operations.add(a=5, b=3.2)
    is_valid: bool = validators.check_numbers(value=result)

    if is_valid:
        print(result)


if __name__ == "__main__":

    print("This is relative_import.py")

    main()
