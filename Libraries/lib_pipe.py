from pipe import select, where


def list_square_even_numbers(num_range: int) -> list[int]:
    num_list = range(num_range)
    result: list[int] = list(
        num_list | where(lambda x: x % 2 == 0) | select(lambda x: x**2)
    )
    return result


def main() -> None:
    while (
        text := input(
            "Input number to display list of square of even numbers or 'q' to quit: "
        )
    ) != "q":
        if text.isdigit():
            square_even_numbers: list[int] = list_square_even_numbers(int(text))
            print(
                f"List of square of even numbers of input {text} is: {square_even_numbers}"
            )
        else:
            print("Invalid Input!")


if __name__ == "__main__":
    main()
