Calculator
==========

A stateful Calculator class implemented in calculator.py which emulates handheld calculator behavior by quantizing (rounding) after each operation to the configured precision; get_total() returns the current rounded total.

Features
- Stateful running total
- Operations: add, subtract, multiply, divide, percent, percent_add, percent_substract
- Undo most recent operation with clear()
- Reset everything with clear_all()
- Show total with get_total()  
- Configurable precision and max_value via constructor (precision default: 2, max_value default: 100000)

Quick usage example

```python
from calculator import Calculator
calc = Calculator(precision=2, max_value=1000)
calc.add(1) 
calc.add(2)
calc.add(3.333)
calc.add(100)
calc.clear() # User realises they made an error
calc.add(10) # User adds correct value
print(calc.get_total())  # -> 16.33
calc.clear_all()
print(calc.get_total())  # -> 0.00
```

Running tests (focused)

To run only the calculator tests used during development:

```bash
pytest -q
```

