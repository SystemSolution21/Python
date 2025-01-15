import math


class InventoryItem:
    """Custom Inventory Item using class magic methods"""

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} @ ${self.price} x {self.quantity}"

    def __repr__(self):
        return f"InventoryItem({self.name}, {self.price}, {self.quantity})"

    # Arithmetic Operators
    def __add__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem(self.name, self.price, self.quantity + other.quantity)
        return "Cannot add the items of different types or names"

    def __sub__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            if self.quantity >= other.quantity:
                return InventoryItem(
                    self.name, self.price, self.quantity - other.quantity
                )
            return f"Cannot subtract '{other.quantity}' more than the available quantity '{self.quantity}'"
        return f"Cannot subtract items '{other.name}' from different type of items '{self.name}'"

    def __mul__(self, factor):
        if isinstance(factor, (int, float)):
            return InventoryItem(self.name, self.price, int(self.quantity * factor))
        raise ValueError("Multiplication factor must be number!")

    def __truediv__(self, factor):
        if isinstance(factor, (int, float)) and factor != 0:
            return InventoryItem(self.name, self.price, int(self.quantity / factor))
        raise ZeroDivisionError("Division factor must be non-zero number!")

    # Comparison Operators
    def __eq__(self, other: object) -> bool:
        if isinstance(other, InventoryItem):
            return (
                self.name == other.name
                and self.price == other.price
                and self.quantity == other.quantity
            )
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity < other.quantity
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity > other.quantity
        return False


class Fraction:
    """Custom class Fraction using __truediv__ magic method"""

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.simplify()

    def simplify(self):
        gcd = math.gcd(self.numerator, self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd

    def __truediv__(self, other):
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return Fraction(new_numerator, new_denominator)

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"


def inventory_item():
    item1 = InventoryItem("widget", 10.0, 5)
    item2 = InventoryItem("widget", 10.0, 3)
    item3 = InventoryItem("widget", 10.0, 6)
    item4 = InventoryItem("gadget", 15.0, 10)

    print(f"{str(item1) =  }")
    print(f"{repr(item1) =  }")

    print(f"{str(item4) =  }")
    print(f"{repr(item4) =  }")

    # Arithmetic Operation
    add_item = item1 + item2
    print(f"{add_item =  }")

    add_item = item1 + item3
    print(f"{add_item =  }")

    sub_item = item1 - item2
    print(f"{sub_item =  }")

    sub_item = item1 - item3
    print(f"{sub_item =  }")

    sub_item = item1 - item4
    print(f"{sub_item =  }")

    try:
        mul_item = item1 * 2.09
        # mul_item = item1 * "2"
        print(f"{mul_item= }")
    except ValueError as e:
        print(e)

    try:
        truediv_item = item1 / 2.09
        # truediv_item = item1 / 0
        print(f"{truediv_item= }")
    except ZeroDivisionError as e:
        print(e)

    # Comparison Operators
    print(f'{item1 == InventoryItem("widget", 10.0, 5) = }')
    print(f"{item1 == item2 = }")

    print(f"{item1 < item2 = }")
    print(f"{item1 < item3 = }")

    print(f"{item1 > item2 = }")
    print(f"{item1 > item3 = }")


def fraction():
    # Fraction
    f1 = Fraction(1, 2)
    f2 = Fraction(3, 4)
    result = f1 / f2
    print(str(result))  # Output: 2/3


def main():
    inventory_item()
    fraction()


if __name__ == "__main__":
    main()
