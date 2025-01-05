import sys
from .math_operations import add


def main() -> None:

    print(sys.path[0])

    print(add(a=1, b=2))


if __name__ == "__main__":

    print("This is relative_import.py")

    main()
