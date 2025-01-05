# Use of Basic Import Statement
import sys
import helpers.math_operations
import utils.validators


def main() -> None:

    print(sys.path[0])

    result: int | float = helpers.math_operations.add(a=5, b=3.2)
    is_valid: bool = utils.validators.check_numbers(value=result)

    if is_valid:
        print(result)


if __name__ == "__main__":

    print("This is the basic_import.py")

    main()
