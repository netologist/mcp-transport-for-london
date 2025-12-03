# 🚍 MCP Server for Transport for London (TFL)

London Bus MCP Server providing real-time London bus information via Transport for London (TfL) API.

## Overview

This project implements a Model Context Protocol (MCP) server that exposes London bus stop information through FastMCP. It includes:

- **MCP Server** (`server.py`) - FastMCP server with TfL API integration
- **AI Client** (`client.py`) - Pydantic AI agent that uses the MCP tools
- **Evaluations** (`evaluations.py`) - Test cases and evaluations for the agent

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- Node.js (for MCP Inspector)

## Quick Start

### 1. Install Dependencies

```bash
make install
```

This runs `uv sync` to install all dependencies from `pyproject.toml`.

### 2. Start the MCP Server

```bash
make server
```

The server will be available at `http://127.0.0.1:8000/mcp`

### 3. Test with Client (in another terminal)

```bash
make client
```

This runs the Pydantic AI agent that queries bus stops near Piccadilly Circus.

## Opik Integration (Local Deployment)

This project supports [Opik](https://www.comet.com/docs/opik) for experiment tracking and evaluation. You can run Opik locally using Docker Compose.

### Prerequisites for Opik

- Docker and Docker Compose installed
- Clone the Opik repository (outside this project):

```bash
# Clone the Opik repository
git clone https://github.com/comet-ml/opik.git

# Navigate to the opik folder

cd opik

# Start the Opik platform

./opik.sh

# Stop the Opik platform
./opik.sh --stop
```

Opik will be available at [http://localhost:5173](http://localhost:5173)

### Using Opik with Evaluations

Once Opik is running, your evaluation traces will automatically be logged to the local Opik instance at `http://localhost:5173`.

## Available Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies using `uv sync` |
| `make server` | Start the MCP server |
| `make client` | Run the AI client |
| `make eval` | Run evaluations |
| `make test` | Run all tests |

### Development Commands

| Command | Description |
|---------|-------------|
| `make dev-install` | Install development dependencies |
| `make format` | Format code with black and isort |
| `make lint` | Lint code with ruff |
| `make check` | Run all checks (lint + type check) |
| `make shell` | Open Python shell in uv environment |

### Package Management

| Command | Description |
|---------|-------------|
| `make add PKG=package-name` | Add a package |
| `make add-dev PKG=package-name` | Add a dev package |
| `make lock` | Update uv.lock file |
| `make tree` | Show dependency tree |

### Debugging & Utilities

| Command | Description |
|---------|-------------|
| `make server-debug` | Start server with debug output |
| `make inspector` | Run MCP Inspector |
| `make verify` | Verify server endpoint is accessible |
| `make status` | Check if server is running |
| `make kill-server` | Kill process on port 8000 |

### Cleanup

| Command | Description |
|---------|-------------|
| `make clean` | Clean cache files and build artifacts |
| `make clean-all` | Remove everything including .venv |

## Project Structure

```
tfl-mcp/
├── server.py           # FastMCP server with TfL API integration
├── client.py           # Pydantic AI agent client
├── evaluations.py      # Test cases and evaluations
├── otel.py            # OpenTelemetry configuration
├── pyproject.toml     # Project dependencies and configuration
├── Makefile           # Task automation
└── README.md          # This file
```

## Usage Examples

### Adding New Packages

```bash
# Add a runtime package
make add PKG=requests

# Add a development package
make add-dev PKG=pytest
```

### Development Workflow

```bash
# Install all dependencies including dev tools
make dev-install

# Format your code
make format

# Check code quality
make lint

# Run all checks
make check
```

### Running with MCP Inspector

MCP Inspector provides a web UI to test your MCP server:

```bash
# Terminal 1: Start the server
make server

# Terminal 2: Start MCP Inspector
make inspector
```

Then open your browser to the URL shown by the inspector.

## API Tools

### `search_bus_stops`

Search for bus stops by name or postcode.

**Parameters:**
- `query` (str): Stop name or postcode (e.g., 'Oxford Circus', 'SW1A 1AA')

**Returns:**
- List of matching bus stops with IDs, names, and coordinates

**Example:**
```python
# Using the client
res = agent.run_sync("Find bus stops near Piccadilly Circus")
print(res.output)
```

## Configuration

### Server Configuration

The server runs on `streamable-http` transport by default:

```python
mcp.run(transport="streamable-http")  # Accessible at http://127.0.0.1:8000/sse
```

### Client Configuration

The client connects to the server via HTTP:

```python
tfl_mcp_toolset = FastMCPToolset("http://127.0.0.1:8000/sse")
```

## Troubleshooting

### Server won't start

```bash
# Check if port 8000 is already in use
make status

# Kill existing process
make kill-server

# Try starting again
make server
```

### Connection errors

```bash
# Verify server is accessible
make verify

# Should return SSE stream output
```

### Clean install

```bash
# Remove everything and start fresh
make clean-all
make install
```

## Dependencies

Main dependencies:
- `fastmcp` - FastMCP server framework
- `pydantic-ai` - AI agent framework
- `httpx` - HTTP client for TfL API
- `anthropic` - Claude AI model

Development dependencies:
- `black` - Code formatter
- `isort` - Import sorter
- `ruff` - Fast Python linter
- `mypy` - Type checker

## TfL API

This project uses the Transport for London (TfL) API. No API key is required for basic usage.

API Documentation: https://api.tfl.gov.uk

## License

[Add your license here]

## Contributing

[Add contributing guidelines here]
