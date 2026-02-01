import pytest
from decimal import Decimal

from calculator import Calculator


def test_invalid_inputs_raise_expected_exceptions():
    calc = Calculator(precision=2, max_value=1000)

    # invalid numeric string (hex-like) should raise ValueError
    with pytest.raises(ValueError):
        calc.add("0x10")

    # non-numeric types raise TypeError
    for bad in (b"\x00\x10", None, object()):
        with pytest.raises(TypeError):
            calc.add(bad)


def test_overflow_restores_previous_total_and_raises():
    calc = Calculator(precision=2, max_value=1000)
    calc.add(300)
    calc.add(300)
    assert calc.get_total() == Decimal("600.00")

    # adding 600 would exceed max_value (1000) -> raise and total remains unchanged
    with pytest.raises(ValueError):
        calc.add(600)
    assert calc.get_total() == Decimal("600.00")


def test_divide_by_zero_raises_and_does_not_change_total():
    calc = Calculator(precision=2, max_value=1000)
    calc.add(10)
    before = calc.get_total()
    with pytest.raises(ValueError):
        calc.divide(0)
    # total should be unchanged after failed divide
    assert calc.get_total() == before


def test_accepts_various_numeric_types_and_returns_decimal():
    from decimal import Decimal as D

    calc = Calculator(precision=2, max_value=1000)
    calc.add(1)               # int
    calc.add(2.5)             # float (converted via str)
    calc.add("3.25")          # numeric string
    calc.add(D("0.25"))       # Decimal
    # totals: 1 + 2.5 -> 3.5 (quantized), +3.25 -> 6.75, +0.25 -> 7.00
    assert calc.get_total() == D("7.00")
    # get_total returns a Decimal
    assert isinstance(calc.get_total(), D)