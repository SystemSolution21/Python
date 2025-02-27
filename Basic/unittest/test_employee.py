import unittest
from unittest.mock import patch
from employee import Employee


class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("setUpClass")

    @classmethod
    def tearDownClass(cls) -> None:
        print("tearDownClass")

    def setUp(self) -> None:
        print("setUp")
        self.emp1 = Employee(fname="Corey", lname="Schafer", pay=50000)
        self.emp2 = Employee(fname="Sue", lname="Smith", pay=60000)

    def tearDown(self) -> None:
        print("tearDown\n")

    def test_init(self) -> None:
        print("test_init")
        self.assertEqual(first=self.emp1.fname, second="Corey")
        self.assertEqual(first=self.emp1.lname, second="Schafer")
        self.assertEqual(first=self.emp1.pay, second=50000)
        self.assertEqual(first=self.emp2.fname, second="Sue")
        self.assertEqual(first=self.emp2.lname, second="Smith")
        self.assertEqual(first=self.emp2.pay, second=60000)

    def test_fullname(self) -> None:
        print("test_fullname")
        self.assertEqual(first=self.emp1.fullname, second="Corey Schafer")
        self.assertEqual(first=self.emp2.fullname, second="Sue Smith")

        self.emp1.fname = "John"
        self.emp2.fname = "Jane"

        self.assertEqual(first=self.emp1.fullname, second="John Schafer")
        self.assertEqual(first=self.emp2.fullname, second="Jane Smith")

    def test_email(self) -> None:
        print("test_email")
        self.assertEqual(first=self.emp1.email, second="corey.schafer@company.com")
        self.assertEqual(first=self.emp2.email, second="sue.smith@company.com")

        self.emp1.fname = "John"
        self.emp2.fname = "Jane"

        self.assertEqual(first=self.emp1.email, second="john.schafer@company.com")
        self.assertEqual(first=self.emp2.email, second="jane.smith@company.com")

    def test_pay_raise(self) -> None:
        print("test_pay_raise")
        self.emp1.pay_raise()
        self.emp2.pay_raise()

        self.assertEqual(first=self.emp1.pay, second=52500)
        self.assertEqual(first=self.emp2.pay, second=63000)

    def test_monthly_schedule(self) -> None:

        with patch("employee.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "Success"

            schedule: str = self.emp1.monthly_schedule(month="May")
            mocked_get.assert_called_with("http://company.com/Schafer/May")
            self.assertEqual(first=schedule, second="Success")

            mocked_get.return_value.ok = False

            schedule = self.emp2.monthly_schedule(month="June")
            mocked_get.assert_called_with("http://company.com/Smith/June")
            self.assertEqual(first=schedule, second="Bad Response!")


if __name__ == "__main__":
    unittest.main()
