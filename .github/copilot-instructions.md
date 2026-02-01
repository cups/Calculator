Build, test, and lint commands

- Run the full test suite:
  - pytest -q
- Run the focused calculator tests used during development:
  - pytest -q test_calculator.py
- Run a single test function or class:
  - pytest -q test_calculator.py::test_function_name
  - or target any test file: pytest -q path/to/test_file.py::TestClass::test_method
- Linting: no project linter configured. Add and run a linter (recommended):
  - pip install flake8
  - flake8 .

High-level architecture

- Purpose: small, stateful Calculator implemented in calculator.py for TDD learning and small utilities.
- Core component: Calculator class (calculator.py)
  - Stores totals as Decimal instances, quantized to a configured precision after each operation (per-operation quantization).
  - Constructor: Calculator(precision: int = 2, max_value: Number = 1000)
  - Public API (used by tests):
    - add(value)
    - subtract(value) (alias: minus may exist in some implementations)
    - multiply(factor)
    - divide(divisor)
    - get_total() -> Decimal (current quantized total)
    - clear() -> one-shot undo (restores the previous total and clears the undo)
    - clear_all() -> reset total and undo to zero
  - Internals:
    - _total: Decimal (always quantized to configured precision)
    - _last_total: Optional[Decimal] (used for single undo)
    - _to_decimal(): converts inputs (int, float via str, Decimal, numeric str) to Decimal; raises TypeError for unsupported types and ValueError for invalid numeric strings
    - Rounding: uses Decimal.quantize with ROUND_HALF_EVEN (banker's rounding)
    - max_value: enforced as magnitude limit; exceeding it raises ValueError and restores previous total

Key conventions and repository-specific patterns

- Per-operation quantization: the Calculator intentionally rounds after every operation to the configured precision; tests expect this behavior and use Decimal assertions (e.g., Decimal("6.33")).
- Decimal handling: floats are converted via str to Decimal to avoid binary artifacts; tests assert Decimal equality, not floats.
- One-shot undo semantics: clear() is single-use; clear_all() fully resets state.
- Error semantics:
  - TypeError for unsupported input types (bytes, None, arbitrary objects)
  - ValueError for invalid numeric strings (e.g., "0x10"), division by zero, and overflow (exceeding max_value)
- Tests are the canonical source of behavior; prefer making small changes and running the focused tests (pytest -q test_calculator.py) before running the full suite.
- Pull request guideline from local docs: when proposing code changes, keep edits minimal and reference absolute line numbers in review descriptions (this project historically requested that).

Files of interest (quick guide)

- calculator.py — implementation of Calculator
- test_calculator.py, test_arithmetic.py, test_inputs_and_errors.py — the test suite that documents and enforces behavior
- README.md and copilot-instructions.md (root) — short project docs and development notes

AI assistant and other tooling files to check

- This repo currently has a root copilot-instructions.md; this new file is intended to complement it under .github so Copilot CLI sessions can find repository-specific instructions.
- No other AI assistant config files (CLAUDE.md, .cursorrules, AGENTS.md, etc.) were detected; if added, include important behavioral notes here.

Notes for future Copilot sessions

- Use tests as the single source of truth. If behavior differs between README examples and tests (e.g., "total()" vs "get_total()"), follow the tests and update README/docs accordingly.
- When changing numeric handling or rounding behavior, update tests that assert Decimal values and include focused test runs.
- Keep changes minimal and run pytest -q test_calculator.py as the quick feedback loop.
