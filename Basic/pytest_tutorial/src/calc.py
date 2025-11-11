def add(x: int, y: int) -> int:
    """Addition

    Args:
        x (int): parameter1
        y (int): parameter2

    Returns:
        int: added x and y
    """
    return x + y


def subtract(x: int, y: int) -> int:
    """Subtraction

    Args:
        x (int): parameter1
        y (int): parameter2

    Returns:
        int: Subtract y from x
    """
    return x - y


def multiply(x: int, y: int) -> int:
    """Multiplication

    Args:
        x (int): parameter1
        y (int): parameter2

    Returns:
        int: Multiply x with Y
    """
    return x * y


def divide(x: int, y: int) -> int:
    """Division

    Args:
        x (int): parameter1
        y (int): parameter2

    Returns:
        int: Divide x by Y
    """
    if y == 0:
        raise ValueError("Can not divide by zero!")
    return x // y
