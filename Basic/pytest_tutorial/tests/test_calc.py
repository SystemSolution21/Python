import pytest
from src.calc import add, divide, multiply, subtract


class TestCalc:
    def test_add(self):
        """Test the add function with various inputs"""
        # Test positive integers
        assert add(1, 2) == 3
        assert add(5, 7) == 12

        # Test with zero
        assert add(0, 5) == 5
        assert add(10, 0) == 10
        assert add(0, 0) == 0

        # Test negative numbers
        assert add(-1, -2) == -3
        assert add(-5, 5) == 0
        assert add(10, -5) == 5

    def test_subtract(self):
        """Test the subtract function with various inputs"""
        # Test positive integers
        assert subtract(5, 3) == 2
        assert subtract(10, 7) == 3

        # Test with zero
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5
        assert subtract(0, 0) == 0

        # Test negative numbers
        assert subtract(-1, -2) == 1
        assert subtract(-5, 5) == -10
        assert subtract(10, -5) == 15

    def test_multiply(self):
        """Test the multiply function with various inputs"""
        # Test positive integers
        assert multiply(2, 3) == 6
        assert multiply(5, 7) == 35

        # Test with zero
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0
        assert multiply(0, 0) == 0

        # Test negative numbers
        assert multiply(-2, 3) == -6
        assert multiply(2, -3) == -6
        assert multiply(-2, -3) == 6

    def test_divide(self):
        """Test the divide function with various inputs"""
        # Test positive integers
        assert divide(6, 3) == 2
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3

        # Test with integer division results
        assert divide(5, 2) == 2  # Integer division: 5 // 2 = 2
        assert divide(10, 3) == 3  # Integer division: 10 // 3 = 3

        # Test negative numbers
        assert divide(-6, 3) == -2
        assert divide(6, -3) == -2
        assert divide(-6, -3) == 2

    def test_divide_by_zero(self):
        """Test that divide raises ValueError when dividing by zero"""
        with pytest.raises(expected_exception=ValueError) as excinfo:
            divide(x=10, y=0)
        assert "Can not divide by zero!" in str(object=excinfo.value)

    @pytest.mark.parametrize(
        argnames="x, y, expected",
        argvalues=[(1, 1, 1), (5, 2, 2), (10, 5, 2), (7, 2, 3), (100, 10, 10)],
    )
    def test_divide_parametrized(self, x, y, expected):
        """Test divide function with parametrized inputs"""
        assert divide(x=x, y=y) == expected

    @pytest.mark.parametrize(
        argnames="func, x, y, expected",
        argvalues=[
            (add, 1, 2, 3),
            (subtract, 5, 3, 2),
            (multiply, 2, 3, 6),
            (divide, 6, 3, 2),
        ],
    )
    def test_all_functions(self, func, x, y, expected):
        """Test all calculator functions with parametrized inputs"""
        assert func(x, y) == expected
