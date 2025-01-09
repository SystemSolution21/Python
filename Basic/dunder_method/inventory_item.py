class InventoryItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} @ ${self.price} x {self.quantity}"

    def __repr__(self):
        return f"InventoryItem({self.name}, {self.price}, {self.quantity})"

    def __add__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem(self.name, self.price, self.quantity + other.quantity)
        return "Can't add the items of different types or names"


def main():
    item1 = InventoryItem("widget", 10.0, 5)
    item2 = InventoryItem("widget", 10.0, 3)
    item3 = InventoryItem("gadget", 15.0, 10)

    print(f"{str(item1) =  }")
    print(f"{repr(item1) =  }")

    print(f"{str(item3) =  }")
    print(f"{repr(item3) =  }")

    add_item = item1 + item2
    print(f"{add_item =  }")

    add_item = item1 + item3
    print(f"{add_item =  }")


if __name__ == "__main__":
    main()
