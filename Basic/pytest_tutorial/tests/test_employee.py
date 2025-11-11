from typing import Callable, Generator

import pytest
from pytest_mock import MockerFixture
from src.employee import Employee


class TestEmployee:
    @pytest.fixture
    def employee(self) -> Employee:
        """Fixture to create a sample employee for tests"""
        return Employee(fname="John", lname="Doe", pay=50000)

    def test_init(self, employee: Employee) -> None:
        """Test employee initialization"""
        assert employee.fname == "John"
        assert employee.lname == "Doe"
        assert employee.pay == 50000

    def test_fullname(self, employee: Employee) -> None:
        """Test the fullname property"""
        assert employee.fullname == "John Doe"

        # Test with different values
        employee.fname = "Jane"
        assert employee.fullname == "Jane Doe"

    def test_email(self, employee: Employee) -> None:
        """Test the email property"""
        assert employee.email == "john.doe@company.com"

        # Test with different values
        employee.fname = "Jane"
        assert employee.email == "jane.doe@company.com"

    def test_pay_raise(self, employee: Employee) -> None:
        """Test the pay_raise method"""
        initial_pay: int = employee.pay
        expected_pay = int(initial_pay * Employee.pay_raise_rate)

        employee.pay_raise()
        assert employee.pay == expected_pay

        # Test with a different pay_raise_rate
        Employee.pay_raise_rate = 1.10
        employee.pay_raise()
        assert employee.pay == int(expected_pay * 1.10)

        # Reset pay_raise_rate for other tests
        Employee.pay_raise_rate = 1.05

    def test_pay_raise_rate_class_variable(self) -> None:
        """Test that pay_raise_rate is a class variable"""
        emp1 = Employee(fname="John", lname="Doe", pay=50000)
        emp2 = Employee(fname="Jane", lname="Smith", pay=60000)

        Employee.pay_raise_rate = 1.10
        assert emp1.pay_raise_rate == 1.10
        assert emp2.pay_raise_rate == 1.10

        # Reset pay_raise_rate for other tests
        Employee.pay_raise_rate = 1.05

    def test_monthly_schedule_success(
        self,
        employee: Employee,
        mocker: Callable[..., Generator[MockerFixture, None, None]],
    ) -> None:
        """Test monthly_schedule method with a successful response"""
        # Configure the mock
        mock_get = mocker.patch("src.employee.requests.get")
        mock_get.return_value.ok = True
        mock_get.return_value.text = "Success Schedule"

        # Call the method
        schedule: str = employee.monthly_schedule(month="May")

        # Assert the result
        mock_get.assert_called_with("http://company.com/Doe/May")
        assert schedule == "Success Schedule"

    def test_monthly_schedule_failure(
        self,
        employee: Employee,
        mocker: Callable[..., Generator[MockerFixture, None, None]],
    ) -> None:
        """Test monthly_schedule method with a failed response"""
        # Configure the mock
        mock_get = mocker.patch("src.employee.requests.get")
        mock_get.return_value.ok = False

        # Call the method
        schedule: str = employee.monthly_schedule(month="June")

        # Assert the result
        mock_get.assert_called_with("http://company.com/Doe/June")
        assert schedule == "Bad Response!"


if __name__ == "__main__":
    pytest.main()
