.PHONY: start check fmt fmt-check

start:
	uv run stockboard/main.py

check:
	uv run ty check

fmt-check:
	uv run ruff check

fmt:
	uv run ruff check --fix
