import pytest
from decimal import Decimal

from calculator import Calculator


def test_percent_and_undo():
    calc = Calculator(precision=2, max_value=1000)
    # build to 1000
    calc.add(500)
    calc.add(500)
    assert calc.get_total() == Decimal("1000.00")

    # percent 27 should set total to 270.00
    calc.percent(27)
    assert calc.get_total() == Decimal("270.00")

    # undo should restore previous total (1000.00)
    calc.clear()
    assert calc.get_total() == Decimal("1000.00")

    # percent should accept string inputs as well
    calc.percent("10")
    assert calc.get_total() == Decimal("100.00")


def test_percent_add_and_overflow_and_undo():
    calc = Calculator(precision=2, max_value=1000)
    # small build
    calc.add(30)
    calc.add(30)
    assert calc.get_total() == Decimal("60.00")

    # percent_add 10% should add 6 -> 66
    calc.percent_add(10)
    assert calc.get_total() == Decimal("66.00")

    # undo restores previous total 60
    calc.clear()
    assert calc.get_total() == Decimal("60.00")

    # overflow: add 900 to make 960, percent_add 10% would try to make 1056 -> should raise
    calc.add(900)
    assert calc.get_total() == Decimal("960.00")
    with pytest.raises(ValueError):
        calc.percent_add(10)
    # total should remain unchanged after failed percent_add
    assert calc.get_total() == Decimal("960.00")


def test_percent_substract_and_undo():
    calc = Calculator(precision=2, max_value=1000)
    calc.add(40)
    calc.add(40)
    assert calc.get_total() == Decimal("80.00")

    # percent_substract 10% should subtract 8 -> 72
    calc.percent_substract(10)
    assert calc.get_total() == Decimal("72.00")

    # undo restores previous total 80
    calc.clear()
    assert calc.get_total() == Decimal("80.00")


def test_percent_with_small_max_and_overflow_behavior():
    # set max_value to 100 to exercise behavior near limits
    calc = Calculator(precision=2, max_value=100)
    calc.add(60)
    calc.add(30)
    assert calc.get_total() == Decimal("90.00")

    # percent_add 20% would try to increase by 18 -> 108 which exceeds max -> should raise
    with pytest.raises(ValueError):
        calc.percent_add(20)
    # total remains unchanged after failed operation
    assert calc.get_total() == Decimal("90.00")

    # percent_substract with negative percent should still compute; using -10 should increase total
    with pytest.raises(ValueError):
        # this will attempt to add 9 (since subtracting -10% is adding), resulting in 99 -> OK
        # but try a larger negative to overflow
        calc.percent_substract(-50)

    # percent to set absolute percentage: trying percent(150) would set total to 135 -> overflow
    with pytest.raises(ValueError):
        calc.percent(150)
    assert calc.get_total() == Decimal("90.00")
