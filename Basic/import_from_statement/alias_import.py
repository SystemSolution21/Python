# Use Import Alias
import sys
import helpers.math_operations as math_ops
import utils.validators as valid


def main() -> None:
    print(sys.path[0])

    result: int | float = math_ops.add(a=5, b=2)
    is_valid: bool = valid.check_numbers(value=result)

    if is_valid:
        print(result)


if __name__ == "__main__":

    print("This is alias_import.py")

    main()
