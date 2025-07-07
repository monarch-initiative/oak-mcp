# OAK MCP - Makefile for development and testing
#
# Manual setup without make:
#   uv sync                                    # install dependencies
#   uv pip install -e .                       # install in dev mode
#   uv run pytest tests/ -v                   # run tests
#   uv run python src/oak_mcp/main.py         # run MCP server
#
# Claude Desktop config:
#   Add to ~/Library/Application Support/Claude/claude_desktop_config.json:
#   {
#     "mcpServers": {
#       "oak-mcp": {
#         "command": "uv",
#         "args": ["run", "python", "src/oak_mcp/main.py"],
#         "cwd": "/path/to/oak-mcp"
#       }
#     }
#   }
#
# Claude Code MCP setup:
#   claude mcp add -s project oak-mcp uv run python src/oak_mcp/main.py
#
# Goose setup:
#   goose session --with-extension "uv run python src/oak_mcp/main.py"

.PHONY: install test clean dev-install run-server check-deps dev test-mcp-extended

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
	@echo "Testing MCP protocol handshake..."
	echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "1.0", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}, "id": 1}' | timeout 3 uv run python src/oak_mcp/main.py 2>/dev/null | head -1

test-mcp-extended:
	@echo "Testing MCP protocol initialization..."
	@(echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "1.0", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}, "id": 1}'; \
	 echo '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 2}'; \
	 echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "search_ontology_with_oak", "arguments": {"term": "cancer", "ontology": "ols:mondo", "n": 2}}, "id": 3}') | \
	timeout 5 uv run python src/oak_mcp/main.py 2>/dev/null | head -10

# Development workflow
dev: clean install dev-install test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true