# oak_mcp

A model context protocol (MCP) to help agents interact with ontologies and the ontology access kit

## Quick Start

```bash
# Install dependencies and set up development environment
make dev

# Run the MCP server
make run-server

# Run tests
make test
```

## Installation

```bash
# Install in development mode (includes dependencies)
make dev-install
```

## Usage

### Testing MCP Protocol

```bash
make test-mcp
```

### Integration with AI Tools

#### Claude Desktop

Add this to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "oak-mcp": {
      "command": "uv",
      "args": ["run", "python", "src/oak_mcp/main.py"],
      "cwd": "/path/to/oak-mcp"
    }
  }
}
```

#### Claude Code

```bash
claude mcp add -s project oak-mcp uv run python src/oak_mcp/main.py
```

#### Goose

```bash
goose session --with-extension "uv run python src/oak_mcp/main.py"
```

## Development

```bash
# Full development setup
make dev

# Run tests
make test

# Check dependencies
make check-deps

# Clean build artifacts
make clean
```

## License

BSD-3-Clause
