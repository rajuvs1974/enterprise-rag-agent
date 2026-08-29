.PHONY: test lint typecheck check

test:
	uv run pytest

lint:
	uv run ruff check .

typecheck:
	uv run mypy src

format:
	uv run ruff format --check .
check:
	uv run ruff format --check .  
	uv run ruff check .
	uv run mypy src
	uv run pytest