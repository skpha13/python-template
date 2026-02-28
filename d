#!/bin/bash

echo -e "\033[1;34m==> Running: ruff format src\033[0m"
uv run ruff format src || true

echo -e "\033[1;34m==> Running: ruff check src --fix\033[0m"
uv run ruff check src --fix || true

echo -e "\033[1;34m==> Running: mypy src\033[0m"
uv run mypy src