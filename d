#!/bin/bash
set -e

echo -e "\033[1;34m==> Running: ruff format src\033[0m"
uv run ruff format src

echo -e "\033[1;34m==> Running: ruff check src --fix\033[0m"
uv run ruff check src --fix

echo -e "\033[1;34m==> Running: mypy src\033[0m"
uv run mypy src