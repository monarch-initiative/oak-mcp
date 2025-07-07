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

### Using uvx (Recommended)

```bash
# Install and run directly with uvx
uvx oak-mcp
```

### Development Installation

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
      "type": "stdio",
      "command": "uvx",
      "args": [
        "oak-mcp"
      ],
      "env": {}
    }
  }
}
```

#### Claude Code

```bash
claude mcp add oak-mcp uvx oak-mcp
```

#### Goose

```bash
goose session --with-extension "uvx oak-mcp"
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
