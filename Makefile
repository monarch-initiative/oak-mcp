.PHONY: test-coverage clean install dev format lint all server build upload-test upload release deptry mypy test-mcp test-mcp-extended test-medical-integration test-real-world-integration

# Default target
all: clean install dev test-coverage format lint mypy deptry build test-mcp test-mcp-extended test-medical-integration test-real-world-integration

# Install everything for development
dev:
	uv sync --group dev

# Install production only
install:
	uv sync

# Run tests with coverage
test-coverage:
	uv run pytest --cov=oak_mcp --cov-report=html --cov-report=term tests/

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf src/*.egg-info

# Run server mode
server:
	uv run python src/oak_mcp/main.py

# Format code with black
format:
	uv run black src/ tests/

lint:
	uv run ruff check --fix src/ tests/

# Check for unused dependencies
deptry:
	uvx deptry .

# Type checking
mypy:
	uv run mypy src/

# Build package with hatch
build:
	uv run hatch build

# Upload to TestPyPI (using token-based auth)
upload-test:
	uv run twine upload --repository testpypi dist/*

# Upload to PyPI (using token-based auth - set TWINE_PASSWORD environment variable first)
upload:
	uv run twine upload dist/*

# Complete release workflow
release: clean test-coverage build upload

# Medical AI Integration Testing
test-medical-integration:
	@echo "🔬 Testing medical AI integration..."
	uv run pytest tests/test_real_world_integration.py::test_diabetes_research_workflow -v -s

test-real-world-integration:
	@echo "🌍 Testing real-world integration..."
	uv run pytest tests/test_real_world_integration.py -v

test-cardiac-phenotypes:
	@echo "❤️ Testing cardiac phenotype discovery..."
	uv run pytest tests/test_real_world_integration.py::test_cardiac_phenotype_discovery -v -s

test-cancer-research:
	@echo "🎯 Testing cancer research workflow..."
	uv run pytest tests/test_real_world_integration.py::test_cancer_relevancy_ranking -v -s

test-cross-ontology:
	@echo "🧠 Testing cross-ontology search..."
	uv run pytest tests/test_real_world_integration.py::test_cross_ontology_brain_research -v -s

test-clinical-workflow:
	@echo "🏥 Testing clinical decision support..."
	uv run pytest tests/test_real_world_integration.py::test_clinical_decision_support_workflow -v -s

# Demo medical functionality  
demo-medical:
	@echo "🚀 OAK-MCP MEDICAL AI DEMO"
	@echo "=========================="
	uv run python -c "import asyncio; from oak_mcp.main import search; asyncio.run(search.fn('diabetes', 'mondo', 3))" | head -10
	@echo ""
	@echo "✅ Oak-MCP provides structured medical knowledge for AI agents!"

# MCP Server testing
test-mcp:
	@echo "Testing MCP protocol handshake..."
	echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "1.0", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}, "id": 1}' | timeout 3 uv run python src/oak_mcp/main.py 2>/dev/null | head -1

test-mcp-extended:
	@echo "Testing MCP protocol initialization..."
	@(echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}, "id": 1}'; \
	 sleep 0.1; \
	 echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 2}'; \
	 sleep 0.1; \
	 echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "search_ontology_with_oak", "arguments": {"term": "cancer", "ontology": "ols:mondo", "n": 2}}, "id": 3}') | \
	timeout 5 uv run python src/oak_mcp/main.py 2>/dev/null | head -10

# OAK MCP - Claude Desktop config:
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