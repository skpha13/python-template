# python-template

## Setup 

This project is based on the [uv](https://docs.astral.sh/uv/) Python package and project manager. 

Some starting commands to help:

- `uv add`: Add a dependency to the project.
- `uv remove`: Remove a dependency from the project.
- `uv sync`: Sync the project's dependencies with the environment.
- `uv lock`: Create a lockfile for the project's dependencies.
- `uv run`: Run a command in the project environment.

How to set up and run the project:

```bash
uv venv # create a new virtual environment
uv pip install -e . # install the current project in editable mode
uv run src/main.py # run the sample template file
```

## Linters and Type Checking

This project uses [ruff](https://docs.astral.sh/ruff/) as a linter and formatter and [mypy](https://mypy.readthedocs.io/en/stable/) for type checking. 

We provide a simple bash script to run linting and type checking all at once:

```bash
./d
```