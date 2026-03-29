# python-template

## Requirements

- Python 3.12 or newer (`requires-python` in `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) installed on your PATH

## Setup

This project is based on the [uv](https://docs.astral.sh/uv/) Python package and project manager. 

Useful commands:

- `uv add`: Add a dependency to the project.
- `uv remove`: Remove a dependency from the project.
- `uv sync`: Sync the project's dependencies with the environment.
- `uv lock`: Create a lockfile for the project's dependencies.
- `uv run`: Run a command in the project environment.

Initial setup and run:

```bash
uv venv                    # create a virtual environment (if you do not use the default uv workflow)
uv pip install -e .        # install this project in editable mode
uv run src/main.py         # run the sample entrypoint
```

Install tooling used by `./d` and optional tests:

```bash
uv sync --group dev        # ruff, mypy, pytest (or use `uv sync --all-groups`)
```

## Linters and type checking

[ruff](https://docs.astral.sh/ruff/) is the linter and formatter; [mypy](https://mypy.readthedocs.io/en/stable/) performs strict type checking (see `pyproject.toml`).

After `uv sync --group dev`, run everything in one step:

```bash
./d
```

## Package customization

The template ships with a top-level package directory named `src` and a distribution name `python-template`. To turn this into your own package in one step, use `scripts/rename_project.sh`.

**What it does**

- Renames the package directory `src/` to the name you provide (for example `my_app`).
- Sets the project name in `pyproject.toml` to a hyphenated form (`my_app` -> `my-app`).
- Updates `from src.` / `import src.` references in Python files under the renamed folder.
- Replaces the string `python-template` with the new hyphenated project name where it appears in those files.
- Adjusts `pyproject.toml` package discovery entries and paths in the `d` script so ruff and mypy still target the right tree.

**How to run it**

Interactive prompt:

```bash
./scripts/rename_project.sh
```

Non-interactive (same validation rules apply):

```bash
./scripts/rename_project.sh my_app
```

**Rules**

- Must be a valid Python package name: start with a letter or underscore; only letters, digits, and underscores afterward.
- Cannot be `src` (no-op) or collide with an existing file or directory.

**After renaming**

- Re-sync the environment if needed: `uv pip install -e .` or `uv sync --group dev`.
- Run the app with `uv run <your_package>/main.py` instead of `src/main.py`.
- Update the title at the top of this README and any other docs or CI paths that still say `src` or `python-template` if you use them elsewhere.

The script uses BSD/macOS `sed -i ''` syntax. On GNU/Linux you may need to change those invocations to `sed -i` (no empty argument) in `scripts/rename_project.sh`.

## Environment (`.env`)

Local settings use [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) in `src.config` (`EnvConfig` and `get_settings()`).

- Copy `.env.example` to `.env` in the **project root** (next to `pyproject.toml`). `.env` is gitignored; the example file documents supported keys.
- The `.env` file path is **anchored to the project root** inside `src.config` (`Path` derived from `config.py`), not the shell’s current working directory, so loading behaves the same no matter where you run `uv run` from.

| Variable | Meaning |
|----------|---------|
| `LOG_DIR` | Name of a subdirectory under `logs/` where log files are written. Default: `default`. Must resolve **inside** `logs/` (the app rejects values that try to escape with `..` or absolute paths). |

## Logging

Logging is configured in `configs/logger.yaml` and applied with `logging.config.dictConfig()` when `src.logging_config` is imported.

- The **root** logger gets two handlers: **console** (colored output via [colorlog](https://github.com/borntyping/python-colorlog) on stdout) and **file** (plain text). The YAML is the single schema; the file handler’s path is set in code to:

  `logs/<log_dir>/<YYYY-MM-DD_HH:MM:SS>.log`

  where `<log_dir>` comes from `LOG_DIR` / settings (see above).

- Use `from src.logging_config import logger` for normal log calls.

### `log_performance` decorator

`log_performance` is a **parameterized** decorator: always invoke it with parentheses.

- **`@log_performance()`** — logs when the function **starts** and **finishes**, including elapsed time. No parameter values are logged.
- **`@log_performance(log_args=[...])`** — same timing logs, and the **start** line also includes the listed parameters by **name** and **`repr` value**. Names must match the wrapped function’s parameters. Names that are not part of the signature are skipped.

```python
from src.logging_config import log_performance, logger

@log_performance()
def run_job() -> None:
    ...

@log_performance(log_args=["x", "y"])
def run_with_params(x: int, y: str) -> None:
    ...
```

## Layout

| Path | Role |
|------|------|
| `src/` | Application package until you rename it (see above) |
| `pyproject.toml` | Project metadata, dependencies, ruff/mypy/pytest settings |
| `d` | Helper script: `ruff format`, `ruff check --fix`, `mypy` on the package tree |
| `scripts/rename_project.sh` | One-shot template -> your package name |

## Tests

[pytest](https://docs.pytest.org/) is configured under `[tool.pytest.ini_options]` in `pyproject.toml`. There is no `tests/` tree in the template yet; add one and run:

```bash
uv run pytest
```

## Observations

> [!NOTE]
> This file was documented with the use of LLMs.
