#!/bin/bash

echo ""
echo -e "\033[1;36m───────────────────────────────────────────\033[0m"
echo -e "\033[1;36m  src/                                     \033[0m"
echo -e "\033[1;36m───────────────────────────────────────────\033[0m"
echo ""

echo -e "\033[1;34m==> Running: ruff format src\033[0m"
uv run ruff format src || true

echo -e "\033[1;34m==> Running: ruff check src --fix\033[0m"
uv run ruff check src --fix || true

echo -e "\033[1;34m==> Running: mypy src\033[0m"
uv run mypy src

echo ""
echo -e "\033[1;36m───────────────────────────────────────────\033[0m"
echo -e "\033[1;36m  tests/                                   \033[0m"
echo -e "\033[1;36m───────────────────────────────────────────\033[0m"
echo ""

echo -e "\033[1;34m==> Running: ruff format tests\033[0m"
uv run ruff format tests || true

echo -e "\033[1;34m==> Running: ruff check tests --fix\033[0m"
uv run ruff check tests --fix || true

echo -e "\033[1;34m==> Running: mypy tests\033[0m"
uv run mypy tests
