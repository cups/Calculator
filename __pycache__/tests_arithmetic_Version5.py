import pytest
from decimal import Decimal

from calculator import Calculator


def _sub_method(calc):
    """Return the subtract implementation available on calc (minus or subtract)."""
    if hasattr(calc, "subtract"):
        return calc.subtract
    if hasattr(calc, "minus"):
        return calc.minus
    pytest.skip("Calculator has no subtract/minus method")


def test_add_subtract_multiply_divide_and_precision():
    calc = Calculator(precision=2, max_value=1000)

    # start from zero
    assert calc.get_total() == Decimal("0.00")

    # add sequence and check quantization behavior
    calc.add(1)
    calc.add(2)
    calc.add(3.333)
    assert calc.get_total() == Decimal("6.33")

    # subtract (via available method)
    sub = _sub_method(calc)
    sub(1.33)
    assert calc.get_total() == Decimal("5.00")  # 6.33 - 1.33 -> 5.00

    # multiply / divide
    calc.multiply(2)
    assert calc.get_total() == Decimal("10.00")
    calc.divide(4)
    assert calc.get_total() == Decimal("2.50")

    # rounding: banker's rounding (ROUND_HALF_EVEN)
    calc = Calculator(precision=2, max_value=1000)
    calc.add(1.235)
    assert calc.get_total() == Decimal("1.24")


def test_subtract_alias_and_negative_numbers():
    calc = Calculator(precision=2, max_value=1000)
    calc.add(10)
    # call whichever subtract API is available
    sub = _sub_method(calc)
    sub(3)
    assert calc.get_total() == Decimal("7.00")

    # subtract a larger value -> negative total
    sub(20)
    assert calc.get_total() == Decimal("-13.00")