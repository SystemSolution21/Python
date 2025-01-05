import sys
import helpers as math
import utils as valid


# Importing from the package by initializing __init__.py file.
def main() -> None:
    """
    This function demonstrates how to import from the package
    by initializing __init__.py file.

    :return: None
    """
    result: int | float = math.add(a=5, b=3.2)
    is_valid: bool = valid.check_numbers(value=result)

    if is_valid:
        print(result)


if __name__ == "__main__":

    print("This is package_import.py")

    print(sys.path[0])

    main()
