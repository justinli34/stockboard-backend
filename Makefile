.PHONY: dev check fmt fmt-check

dev:
	uv run watchfiles "uvicorn stockboard.main:app"

check:
	uv run ty check

fmt-check:
	uv run ruff check

fmt:
	uv run ruff check --fix
