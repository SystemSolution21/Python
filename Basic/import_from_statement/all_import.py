# Import Everything using *
import sys
from helpers.math_operations import *


def main() -> None:

    print(sys.path[0])

    # Can directly use functions, but not recommended
    # as it can lead to namespace pollution
    result: int | float = add(a=5, b=3.2)
    print(result)
    result: int | float = sub(a=5.2, b=3)
    print(result)


if __name__ == "__main__":

    print("This is all_import.py")

    main()
