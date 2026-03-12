.PHONY: check fmt fmt-check

check:
	uv run ty check

fmt-check:
	uv run ruff check

fmt:
	uv run ruff check --fix
