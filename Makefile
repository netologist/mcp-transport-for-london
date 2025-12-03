.PHONY: help install clean server client eval test format lint check all

# Variables
UV := uv
PYTHON := uv run python

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)TfL MCP Server - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	@echo "$(GREEN)Installing dependencies with uv...$(NC)"
	$(UV) sync
	@echo "$(GREEN)✓ Installation complete!$(NC)"

init: ## Initialize new project with uv
	@echo "$(GREEN)Initializing project with uv...$(NC)"
	$(UV) init
	@echo "$(GREEN)✓ Initialization complete!$(NC)"

add: ## Add a package (usage: make add PKG=package-name)
	@echo "$(GREEN)Adding package: $(PKG)$(NC)"
	$(UV) add $(PKG)

add-dev: ## Add a dev package (usage: make add-dev PKG=package-name)
	@echo "$(GREEN)Adding dev package: $(PKG)$(NC)"
	$(UV) add --dev $(PKG)

clean: ## Clean up cache files and build artifacts
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

clean-all: clean ## Clean everything including uv cache
	@echo "$(RED)Removing .venv and uv cache...$(NC)"
	rm -rf .venv
	$(UV) cache clean
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

server: ## Start the MCP server (stdio transport for Inspector)
	@echo "$(GREEN)Starting TfL MCP Server (stdio mode)...$(NC)"
	@echo "$(YELLOW)Use 'make server-http' for HTTP mode$(NC)"
	$(UV) run server.py

server-http: ## Start the MCP server (streamable-http on port 8000)
	@echo "$(GREEN)Starting TfL MCP Server (HTTP mode)...$(NC)"
	@echo "$(YELLOW)Server will be available at: http://127.0.0.1:8000$(NC)"
	$(UV) run server.py --http

server-debug: ## Start server with debug output
	@echo "$(GREEN)Starting TfL MCP Server (DEBUG mode)...$(NC)"
	PYTHONUNBUFFERED=1 $(UV) run server.py

client: ## Run the client to test the server
	@echo "$(GREEN)Running TfL MCP Client...$(NC)"
	$(UV) run client.py

eval: ## Run evaluations
	@echo "$(GREEN)Running evaluations...$(NC)"
	$(UV) run evaluations.py

test: ## Run all tests (currently runs evaluations)
	@echo "$(GREEN)Running tests...$(NC)"
	$(UV) run evaluations.py

format: ## Format code with black and isort
	@echo "$(GREEN)Formatting code...$(NC)"
	$(UV) run black server.py client.py evaluations.py otel.py 2>/dev/null || echo "$(YELLOW)black not installed, run: make add-dev PKG=black$(NC)"
	$(UV) run isort server.py client.py evaluations.py otel.py 2>/dev/null || echo "$(YELLOW)isort not installed, run: make add-dev PKG=isort$(NC)"
	@echo "$(GREEN)✓ Formatting complete$(NC)"

lint: ## Lint code with ruff
	@echo "$(GREEN)Linting code...$(NC)"
	$(UV) run ruff check server.py client.py evaluations.py otel.py 2>/dev/null || echo "$(YELLOW)ruff not installed, run: make add-dev PKG=ruff$(NC)"

check: lint ## Run all checks (lint, type check)
	@echo "$(GREEN)Running type checks...$(NC)"
	$(UV) run mypy server.py client.py evaluations.py otel.py 2>/dev/null || echo "$(YELLOW)mypy not installed, run: make add-dev PKG=mypy$(NC)"

dev-install: install ## Install development dependencies
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(UV) add --dev black isort ruff mypy pytest pytest-asyncio
	@echo "$(GREEN)✓ Dev dependencies installed$(NC)"

lock: ## Update uv.lock file
	@echo "$(GREEN)Updating lock file...$(NC)"
	$(UV) lock
	@echo "$(GREEN)✓ Lock file updated$(NC)"

tree: ## Show dependency tree
	@echo "$(GREEN)Dependency tree:$(NC)"
	$(UV) tree


inspector: ## Run MCP Inspector (requires npx)
	@echo "$(GREEN)Starting MCP Inspector...$(NC)"
	@echo "$(YELLOW)Make sure server is running with 'make server' first$(NC)"
	npx @modelcontextprotocol/inspector uv run server.py

inspector-http: ## Run MCP Inspector with HTTP transport (experimental)
	@echo "$(GREEN)Starting MCP Inspector (HTTP mode)...$(NC)"
	@echo "$(YELLOW)Make sure server is running with 'make server-http' first$(NC)"
	npx @modelcontextprotocol/inspector -e ALLOWED_ORIGINS=* --transport http --server-url http://127.0.0.1:8000/mcp

verify: ## Verify server is running and accessible
	@echo "$(GREEN)Verifying server endpoint...$(NC)"
	curl -s -H "Accept: text/event-stream" http://127.0.0.1:8000/mcp | head -n 5 || echo "$(RED)Server not running or not accessible$(NC)"

status: ## Check if server is running
	@echo "$(GREEN)Checking server status...$(NC)"
	@lsof -i :8000 || echo "$(YELLOW)No process listening on port 8000$(NC)"

kill-server: ## Kill any process running on port 8000
	@echo "$(YELLOW)Killing processes on port 8000...$(NC)"
	@lsof -ti :8000 | xargs kill -9 2>/dev/null || echo "$(YELLOW)No process found on port 8000$(NC)"

shell: ## Open a shell in the uv environment
	@echo "$(GREEN)Opening uv shell...$(NC)"
	$(UV) run python

pip-compile: ## Show what pip packages would be installed
	@echo "$(GREEN)Showing pip requirements...$(NC)"
	$(UV) pip compile pyproject.toml

all: install server ## Install dependencies and start server

.DEFAULT_GOAL := help
