# Counter class using dunder methods
class Counter:
    def __init__(self) -> None:
        self.count = 0

    def count_up(self) -> int:
        self.count += 1
        return self.count

    def count_down(self) -> int:
        self.count -= 1
        return self.count

    def __str__(self) -> str:
        return f"Counter: {self.count}"

    def __add__(self, other):
        if isinstance(other, Counter):
            return self.count + other.count
        return "Invalid type"


def main() -> None:
    c1 = Counter()
    c2 = Counter()

    print(f"{str(c1) = } ")
    print(f"{str(c2) = } ")

    print(f"{c1.count_up() = } ")
    print(f"{c1.count_up() = } ")
    print(f"{c2.count_up() = } ")

    print(f"{c1 + c2 = } ")
    print(f"{c1 + 1 = } ")


if __name__ == "__main__":
    main()
