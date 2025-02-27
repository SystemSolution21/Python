import requests


# Create Employee
class Employee:
    """A Sample Employee Class"""

    pay_raise_rate: float = 1.05

    def __init__(self, fname: str, lname: str, pay: int) -> None:
        self.fname: str = fname
        self.lname: str = lname
        self.pay: int = pay

    @property
    def fullname(self) -> str:
        return f"{self.fname} {self.lname}"

    @property
    def email(self) -> str:
        return f"{self.fname.lower()}.{self.lname.lower()}@company.com"

    def pay_raise(self) -> None:
        self.pay = int(self.pay * self.pay_raise_rate)

    def monthly_schedule(self, month) -> str:
        response = requests.get(f"http://company.com/{self.lname}/{month}")
        if response.ok:
            return response.text
        else:
            return "Bad Response!"


if __name__ == "__main__":
    pass
