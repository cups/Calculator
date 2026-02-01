import pytest
from decimal import Decimal

from calculator import Calculator


def test_public_api_basic_operations_and_precision():
    calc = Calculator(precision=2, max_value=1000)
    assert calc.get_total() == Decimal("0.00")

    # Basic adds: add 300 twice -> 600
    calc.add(300)
    calc.add(300)
    assert calc.get_total() == Decimal("600.00")

    # Small legitimate add
    calc.add(0.5)
    assert calc.get_total() == Decimal("600.50")


def test_overflow_raises_and_restores_previous_total():
    calc = Calculator(precision=2, max_value=1000)
    calc.add(300)
    calc.add(300)
    assert calc.get_total() == Decimal("600.00")

    # Adding 600 would exceed max (1000) and must raise ValueError, total stays 600
    with pytest.raises(ValueError):
        calc.add(600)
    assert calc.get_total() == Decimal("600.00")


def test_invalid_inputs_behavior():
    calc = Calculator(precision=2, max_value=1000)

    # valid numeric string
    calc.add("12.34")
    assert calc.get_total() == Decimal("12.34")

    # invalid numeric string (hex) -> ValueError
    with pytest.raises(ValueError):
        calc.add("0x10")

    # bytes, None, arbitrary object -> TypeError
    bad_inputs = [b"\x00\x10", None, object()]
    for bad in bad_inputs:
        with pytest.raises(TypeError):
            calc.add(bad)


def test_multiplication_division_and_divide_by_zero():
    calc = Calculator(precision=2, max_value=1000)
    calc.add(10)
    calc.multiply(2)
    assert calc.get_total() == Decimal("20.00")
    calc.divide(4)
    assert calc.get_total() == Decimal("5.00")

    with pytest.raises(ValueError):
        calc.divide(0)


def test_clear_is_one_shot_undo_and_clear_all():
    calc = Calculator(precision=2, max_value=1000)
    # build 1,2,3 -> 6
    calc.add(1)
    calc.add(2)
    calc.add(3)
    assert calc.get_total() == Decimal("6.00")

    # mistake: add 44 -> 50
    calc.add(44)
    assert calc.get_total() == Decimal("50.00")

    # one-shot clear: restore previous total 6 and forget 44
    calc.clear()
    assert calc.get_total() == Decimal("6.00")

    # calling clear again does nothing (undo was consumed)
    calc.clear()
    assert calc.get_total() == Decimal("6.00")

    # continue working
    calc.add(4)
    assert calc.get_total() == Decimal("10.00")

    # clear_all wipes everything
    calc.clear_all()
    assert calc.get_total() == Decimal("0.00")