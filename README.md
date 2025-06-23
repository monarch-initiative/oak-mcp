# oak_mcp

A model context protocol (MCP) to help agents interact with ontologies and the ontology access kit

## Installation

You can install the package from source:

```bash
pip install -e .
```

Or using uv:

```bash
uv pip install -e .
```

## Usage

You can use the CLI:

```bash
oak-mcp
```

Or import in your Python code:

```python
from oak_mcp.main import create_mcp

mcp = create_mcp()
mcp.run()
```

## Development

### Local Setup

```bash
# Clone the repository
git clone https://github.com/justaddcoffee/oak-mcp.git
cd oak-mcp

# Install development dependencies
uv pip install -e ".[dev]"
```


## License

BSD-3-Clause
