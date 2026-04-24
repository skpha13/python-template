# python-template

## Requirements

- Python 3.12 or newer (`requires-python` in `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) installed on your PATH
- To build the optional **C++ extension**: CMake 3.15 or newer and a C++17 toolchain on your PATH (used by [scikit-build-core](https://scikit-build-core.readthedocs.io/))

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
uv pip install -e .        # install in editable mode (compiles the pybind11 module `_hello_cpp` when toolchains are available)
uv run -m src              # run the package entrypoint (`src/__main__.py`)
```

If the native module is missing (no compiler, skipped build, etc.), the app still starts and logs a hint to rebuild with `uv pip install -e .`.

Install tooling used by `./d` and optional tests:

```bash
uv sync --group dev        # ruff, ty, pytest, pybind11 / scikit-build-core for local builds (or use `uv sync --all-groups`)
```

## Linters and type checking

[ruff](https://docs.astral.sh/ruff/) is the linter and formatter. [ty](https://github.com/astral-sh/ty) performs static type checking (`ty check`); configuration lives under `[tool.ty.environment]` in `pyproject.toml`. Ruff has `F401` (unused imports) marked **unfixable** so automated fixes do not delete imports you still want for side effects.

[Pyright](https://github.com/microsoft/pyright) settings under `[tool.pyright]` are included for editor-based checking; `reportMissingModuleSource` is disabled for the compiled `_hello_cpp` module, which is described to the type checker via `src/hello_world_cpp/_hello_cpp.pyi` until you build the extension.

After `uv sync --group dev`, run everything in one step:

```bash
./d
```

## C++ extension (pybind11)

The template includes a minimal **pybind11** module `_hello_cpp` that exposes `hello_world()` to Python. Sources live under `src/cpp/`; the Python package `src/hello_world_cpp/` imports it and re-exports `hello_world` in `hello_world.py`.

- **Build**: Root `CMakeLists.txt` is driven by **scikit-build-core** (`[build-system]` in `pyproject.toml`). A normal editable install (`uv pip install -e .`) produces the extension next to the package so `from ._hello_cpp import ...` resolves.
- **Types**: `src/hello_world_cpp/_hello_cpp.pyi` stubs the native module for type checkers and Pyright before or without a local compile.
- **Package marker**: `src/py.typed` marks the tree as typed for PEP 561 consumers.

## Package customization

The template ships with a top-level package directory named `src` and a distribution name `python-template`. To turn this into your own package in one step, use `scripts/rename_project.sh`.

**What it does**

- Renames the package directory `src/` to the name you provide (for example `my_app`).
- Sets the project name in `pyproject.toml` to a hyphenated form (`my_app` -> `my-app`).
- Updates `from src.` / `import src.` references in Python files under the renamed folder.
- Replaces the string `python-template` with the new hyphenated project name where it appears in those files.
- Adjusts `pyproject.toml` package discovery entries and paths in the `d` script so ruff and ty still target the right tree.
- Updates `CMakeLists.txt` so C++ paths and the `install(... DESTINATION ...)` prefix match the new package directory (for the pybind11 extension).

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
- Run the app with `uv run -m <your_package>` instead of `uv run -m src`.
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

- Use `from src.logging_config import logger` for normal log calls. Log directory resolution uses `_get_log_dir()` so configured names cannot escape the project `logs/` tree via `..` or absolute paths.

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
| `src/` | Application package until you rename it (see above); run with `uv run -m src` |
| `src/__main__.py` | CLI entry when using `python -m src` / `uv run -m src` |
| `src/hello_world_cpp/` | Python wrapper around `_hello_cpp` |
| `src/cpp/` | C++ sources and bindings for pybind11 |
| `CMakeLists.txt` | CMake project for `_hello_cpp` (used by scikit-build-core) |
| `pyproject.toml` | Project metadata, dependencies, ruff / ty / pyright / pytest settings |
| `d` | Helper script: `ruff format`, `ruff check --fix`, `ty check` on the package tree |
| `scripts/rename_project.sh` | One-shot template -> your package name (including CMake paths) |

## Tests

[pytest](https://docs.pytest.org/) is configured under `[tool.pytest.ini_options]` in `pyproject.toml`. There is no `tests/` tree in the template yet; add one and run:

```bash
uv run pytest
```

## Observations

> [!NOTE]
> This file was documented with the use of LLMs.
