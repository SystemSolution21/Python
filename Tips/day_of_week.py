def day_of_week(num_day: int) -> str:
    """Receive day number and return day name. 

    Args:
        num_day (int): Receive day number

    Returns:
        str: Return day name
    """
    days_dict: dict[int, str] = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday",
    }
    return days_dict.get(num_day, "Invalid day number!")

print(day_of_week(9))
print(day_of_week(3))