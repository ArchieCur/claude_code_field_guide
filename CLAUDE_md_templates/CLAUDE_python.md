# CLAUDE.md — Python Project Template

---

## Project Overview

[What does this project do? Who uses it? What problem does it solve?]

---

## Stack

- **Python version:** 3.11+
- **Package manager:** pip / poetry / uv (pick one, delete others)
- **Testing:** pytest
- **Linting:** ruff
- **Formatting:** black
- **Type checking:** mypy

---

## Development Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Run
python -m [module_name]

# Test
pytest
pytest --cov=src tests/        # with coverage
pytest -x                      # stop on first failure

# Lint & format
ruff check .
ruff check . --fix
black .
mypy src/
```

---

## Project Structure

```
src/
  [package_name]/
    __init__.py
    main.py
    models/
    services/
    utils/
tests/
  conftest.py
  test_[module].py
scripts/
docs/
```

---

## Code Standards

- Type annotations required on all public functions and methods
- Google-style docstrings on all public functions
- No bare `except:` — always catch specific exceptions
- Use `pathlib.Path` not `os.path`
- Use `logging` not `print()`
- Constants in `UPPER_SNAKE_CASE` at module level

---

## Testing Standards

- Minimum coverage target: 80%
- Unit tests for all business logic
- Use `pytest.fixture` for shared setup, not `setUp` methods
- Mock external services — never call real APIs in tests
- Test file naming: `test_[module_name].py`

---

## What NOT to Do

- Do not use mutable default arguments (`def foo(items=[])`)
- Do not import `*` from any module
- Do not commit `.env` files or secrets
- Do not modify auto-generated files in `generated/`
- Do not use deprecated `os.path` functions — use `pathlib`

---

## Environment Variables

All required environment variables are documented in `.env.example`. Copy to `.env` to run locally. Never commit `.env`.

---

## Dependencies

Before adding a new dependency, ask: can the standard library handle this? If adding a dependency, update `requirements.txt` or `pyproject.toml` and document why it was added.
