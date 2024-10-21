
from typing import Any, List

def even_numbers(data_array: Any, /,  max: int, *, min: int=0) -> List[int]:

    """
    Search even number between min and max range from data array and return list of even number.

    Parameters:
    data_array: array of data
    min (int): default minimum range is zero.
    max (int): maximum range is arbitrary.

    returns:
    result (List[int]): return list of even number.
    """
    result: list[int] = []
    for number in data_array:
        if not isinstance(number,(int)):
            continue
        
        is_odd: int = number % 2 !=0
        out_of_range: int = number <= min or number >= max
        if is_odd or out_of_range:
            continue

        result.append(number)

    return sorted(result)

#data_array: list[Any] = [-1, -2, 10, 2, 5, 6, None, "A", 3, 19, 50, 28]
#data_array: tuple = (-1, -2, 2, 5, 6, 8, 3, 19, 50, None, "A", 28)
data_array: set[Any] = {-1, -2, 10, None, "A", 2, 5, 6, 8, 3, 19, 50, 28}
result: List[int] = even_numbers(data_array, min=0, max=100)
print(result)