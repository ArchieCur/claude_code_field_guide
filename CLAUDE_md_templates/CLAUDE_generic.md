# CLAUDE.md — Generic Project Template

This file is read by Claude Code at the start of every session. Be specific — vague instructions produce vague results.

---

## Project Overview

[Describe what this project does in 2-3 sentences. Include the primary language, framework, and purpose.]

Example:
> This is a Python FastAPI service that processes webhook events from Stripe. It validates payloads, updates a PostgreSQL database, and forwards events to an internal message queue.

---

## Architecture

[Describe the key components and how they connect. A simple bullet list is fine.]

- `src/` — application source code
- `tests/` — pytest test suite
- `scripts/` — one-off utility scripts, not production code
- `docs/` — architecture decision records

---

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn src.main:app --reload

# Run tests
pytest

# Lint
ruff check .
```

---

## Code Style

- [Specify formatting rules, e.g. "Black formatting, 88-character line length"]
- [Specify naming conventions, e.g. "snake_case for functions and variables"]
- [Specify type annotation expectations, e.g. "All public functions must have type hints"]
- [Specify docstring format, e.g. "Google-style docstrings for public methods"]

---

## What NOT to Do

- Do not modify files in `generated/` — these are auto-generated and will be overwritten
- Do not commit directly to `main` — always use a feature branch
- Do not add dependencies without updating `requirements.txt`
- Do not use `print()` for logging — use the `logging` module

---

## Testing

- All new features require tests
- Run `pytest` before marking any task complete
- Test files mirror the source structure: `src/foo.py` → `tests/test_foo.py`

---

## Environment

- Python 3.11+
- [Add any other runtime requirements]
- Environment variables are documented in `.env.example`

---

## Key Decisions

[Document any non-obvious architectural choices so Claude doesn't reverse-engineer the wrong conclusion.]

- We use X instead of Y because [reason]
- The `foo` module is intentionally simple — don't refactor it into a class
