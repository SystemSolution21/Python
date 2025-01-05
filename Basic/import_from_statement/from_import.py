# Use of From Import Statement
import sys
from helpers.math_operations import add
from utils.validators import check_numbers


def main() -> None:

    print(sys.path[0])

    result: int | float = add(a=5.2, b=3)
    is_valid: bool = check_numbers(value=result)

    if is_valid:
        print(result)


if __name__ == "__main__":

    print("This is from_import.py")

    main()
