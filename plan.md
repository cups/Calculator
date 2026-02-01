Calculator sub-repo plan

Approach:
- Keep focused tests in test_calculator.py at repo root

Next tasks:
- create 3 percentage operations, percent (of total) percent add (to total) percent subtract(from total)

Behavior note:
- The Calculator intentionally emulates handheld calculator behavior: it quantizes (rounds) after each operation at the configured precision. Tests and documentation should reflect this.

Files of interest:
- calculator.py  (implementation)
- test_calculator.py  (test_ etc)
- README.md
- plan.md

Recommended additional tests to add:
- Full operation flow (add, minus, multiply, divide, percent variants)
- Edge cases (max_value, invalid inputs, divide by zero)
- Undo behavior (clear) and sequence tests (clear_all, percent interactions)

