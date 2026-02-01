## Project

A small stateful Calculator class implemented in calculator.py. This repo is intended for learning and small utility usage.

## Tech stack

- Python
- pytest
- Ubuntu
- gh client

## Method

- Use Test-Driven Development: tests should initially fail and be fixed one at a time (red/green).
- Keep explanations brief: when introducing a new Python idiom, add one sentence explaining it.
- Keep README.md and plan.md current when APIs or file locations change.
- Calculator behavior: this project intentionally emulates handheld calculator behavior by rounding after each operation (per-operation quantization). Update tests and documentation accordingly.

## Code Change Instructions

- When making code changes, provide exact absolute line numbers for any new or modified code blocks so reviewers can locate edits quickly.
- Prefer small, minimal edits and run the focused tests: pytest -q test_calculator.py
- If moving files into a new repo, update plan.md and README.md to reflect the new structure and remote.

## Suggested changes

- add a python linter
