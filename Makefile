# OAK MCP - Code quality and development

.PHONY: install format lint typecheck test run-server qc

# Installation
install:
	uv sync  # Install dependencies from uv.lock and pyproject.toml

# Code quality
format:
	uv run black src/ tests/

format-check:
	uv run black --check src/ tests/

lint:
	uv run ruff check src/ tests/

typecheck:
	uv run mypy src/ tests/

# Testing
test:
	uv run pytest tests/ -v

# Run the MCP server
run-server:
	uv run python src/oak_mcp/main.py

# Run all quality checks
qc: format lint typecheck test