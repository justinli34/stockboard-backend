.PHONY: dev check format

dev:
	uv run watchfiles "uvicorn stockboard.main:app"

check:
	uv run ty check && uv run ruff check

format:
	uv run ruff format
