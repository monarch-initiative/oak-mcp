# OAK MCP - Makefile for development and testing

.PHONY: install test clean dev-install run-server check-deps dev

# Installation
install:
	uv sync

dev-install: install
	uv pip install -e .

# Testing
test:
	uv run pytest tests/ -v

check-deps:
	uv tree

# MCP Server operations
run-server:
	uv run python src/oak_mcp/main.py

test-mcp:
	echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "1.0", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}, "id": 1}' | timeout 3 uv run python src/oak_mcp/main.py 2>/dev/null | head -1

# Development workflow
dev: clean install dev-install test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true