# Repository Guidelines

## Project Structure & Modules
- Core package lives in `src/msc_mcp` (CLI entry in `__main__.py`, MCP tools in `server.py`).
- Tests live in `tests` and use the standard library `unittest` framework.
- Keep new runtime code under `src/msc_mcp`; avoid placing code in `tests` or the repo root except for small utilities.

## Build, Test, and Run
- Create/refresh the environment with `uv sync` (uses `pyproject.toml` and `uv.lock`).
- Run tests with `uv run python -m unittest` (or target a file, e.g. `uv run python -m unittest tests.test_server`).
- Start the MCP server locally with `uv run python -m msc_mcp`.

## Coding Style & Naming
- Use Python 3.10+ type hints where practical and keep functions small and focused.
- Prefer snake_case for functions/variables, PascalCase for classes, and UPPER_SNAKE_CASE for constants.
- Follow the existing formatting style in `server.py`; if in doubt, format with `ruff format` or `black`-like conventions (4‑space indentation, double quotes acceptable but be consistent within a file).

## Testing Guidelines
- Add or update `unittest` cases under `tests`, mirroring the module under test (e.g. `server.py` → `test_server.py`).
- When fixing a bug, first add a failing test, then implement the fix.
- Ensure all tests pass (`uv run python -m unittest`) before opening a PR or sharing changes.

## Commit & Pull Request Practices
- Use clear, imperative commit messages (e.g. `add droidcast install helper`, `fix screenshot encoding error`).
- In PR descriptions, summarize the change, list key commands used to test it, and mention any behavioral or API changes.
- Avoid committing virtual environments or local artifacts; only track source, tests, and configuration files.

## Agent-Specific Instructions
- Do not modify `.venv` or generated lock files unless explicitly requested.
- Prefer minimal, surgical changes that align with existing patterns in `src/msc_mcp` and `tests`.
