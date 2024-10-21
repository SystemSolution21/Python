import datetime
import calendar

# Get day name
def get_day_name(day_num: int) -> str:
    """Convert day number to day name

    Args:
        day_num (int): day number

    Returns:
        str: day name
    """
    # Convert day number to date
    year: int = datetime.date.today().year #Year
    month: int = datetime.date.today().month #Month
    days_in_month: int = calendar.monthrange(year, month)[1] #Days in a month
    
    if days_in_month >= day_num > 0:            
        # Get the day name
        date = datetime.date(year, month, day_num)
        day_name: str = date.strftime("%A")
        return day_name
    else:
        return "Invalid Input!"

def main() -> None:
    while (text := input("Input day number or 'q' to quit: ")) != "q":
        if text.isdigit():
            day_num: int = int(text)
            # Convert day number to day name
            result: str = get_day_name(day_num)
            print(f'The day number {day_num} is {result}')
        else:
            print("Invalid Input!")


if __name__ == "__main__":
    main()
