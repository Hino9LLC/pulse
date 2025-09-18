.PHONY: help setup dev test lint format clean install-uv

help:
	@echo "🚀 Pulse Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  setup        - Complete setup: install deps, create .env, setup React apps"
	@echo "  install-uv   - Install uv package manager if not present"
	@echo ""
	@echo "Development:"
	@echo "  dev          - Start all services (FastAPI + React dashboard)"
	@echo "  dev-api      - Start only FastAPI backend"
	@echo "  dev-dashboard - Start only React dashboard"
	@echo ""
	@echo "Database:"
	@echo "  db-migrate   - Run database migrations"
	@echo "  db-reset     - Reset database (DESTRUCTIVE)"
	@echo ""
	@echo "Code Quality:"
	@echo "  test         - Run all tests (Python + React)"
	@echo "  test-python  - Run only Python tests"
	@echo "  test-react   - Run only React tests"
	@echo "  lint         - Check code style (Python + TypeScript)"
	@echo "  format       - Format code (Python + TypeScript)"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean        - Clean up build artifacts and caches"

# Auto-install uv if not present
install-uv:
	@command -v uv >/dev/null 2>&1 || (echo "📦 Installing uv..." && curl -LsSf https://astral.sh/uv/install.sh | sh)

# Complete setup process
setup: install-uv
	@echo "🔧 Setting up Pulse development environment..."

	# Check Node.js
	@command -v node >/dev/null 2>&1 || (echo "❌ Node.js 18+ required. Please install from https://nodejs.org" && exit 1)
	@echo "✅ Node.js found: $$(node --version)"

	# Python setup
	@echo "📦 Installing Python dependencies..."
	uv sync

	# Create .env if it doesn't exist
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from .env.example..."; \
		cp .env.example .env; \
		echo "⚠️  Please update .env with your configuration"; \
	fi

	# Setup React app
	@echo "⚛️  Setting up React application..."
	cd apps/dashboard && npm install

	@echo "✅ Setup complete! Run 'make dev' to start development"

# Development - start all services
dev:
	@echo "🚀 Starting all services..."
	@echo "  - FastAPI backend: http://localhost:8200"
	@echo "  - Dashboard: http://localhost:3200"
	@echo ""
	@echo "Press Ctrl+C to stop all services"
	@trap 'kill 0' INT; \
	(cd apps/dashboard && npm start) & \
	uv run uvicorn pulse.main:app --reload --host 0.0.0.0 --port 8200 & \
	wait

# Individual service commands
dev-api:
	@echo "🐍 Starting FastAPI backend on http://localhost:8200"
	uv run uvicorn pulse.main:app --reload --host 0.0.0.0 --port 8200

dev-dashboard:
	@echo "⚛️  Starting React dashboard on http://localhost:3200"
	cd apps/dashboard && npm start


# Database operations
db-migrate:
	@echo "🗄️  Running database migrations..."
	uv run alembic upgrade head

db-reset:
	@echo "⚠️  DESTRUCTIVE: Resetting database..."
	@read -p "Are you sure? This will delete all data [y/N]: " confirm && [ "$$confirm" = "y" ]
	rm -f pulse.db
	$(MAKE) db-migrate
	@echo "📊 Loading companies data..."
	uv run python load_companies_data.py

# Testing
test:
	@echo "🧪 Running all tests..."
	@echo "📋 Python tests:"
	@if PYTHONPATH=src uv run pytest; then \
		echo "✅ Python tests passed"; \
	else \
		echo "⚠️  Python test failures found above"; \
	fi
	@echo "📋 React tests:"
	$(MAKE) test-react

test-python:
	@echo "🧪 Running Python tests..."
	PYTHONPATH=src uv run pytest

test-react:
	@echo "📋 Dashboard tests:"
	@if cd apps/dashboard && npm test -- --coverage --silent --watchAll=false; then \
		echo "✅ Dashboard tests passed"; \
	else \
		echo "⚠️  Dashboard test failures found above"; \
	fi

# Code quality
lint:
	@echo "🔍 Running comprehensive Python code quality checks..."
	@echo "📋 Black formatting check:"
	@if uv run black --check src/ tests/; then \
		echo "✅ Black formatting check passed"; \
	else \
		echo "⚠️  Black formatting issues found above"; \
		uv run black src/ tests/; \
	fi
	@echo "📋 Ruff linting check:"
	@if uv run ruff check src/ tests/; then \
		echo "✅ Ruff linting check passed"; \
	else \
		echo "⚠️  Ruff linting errors found above"; \
	fi
	@echo "📋 MyPy type checking:"
	@if uv run mypy src/; then \
		echo "✅ MyPy type checking passed"; \
	else \
		echo "⚠️  MyPy type errors found above"; \
	fi
	@echo "🔍 Checking TypeScript code style..."
	@echo "📋 Dashboard lint check:"
	@if cd apps/dashboard && npm run lint --silent; then \
		echo "✅ Dashboard lint check passed"; \
	else \
		echo "⚠️  Dashboard lint errors found above"; \
	fi

format:
	@echo "🎨 Formatting Python code..."
	uv run black src/ tests/
	uv run ruff check --fix src/ tests/
	@echo "🎨 Formatting TypeScript code..."
	@if cd apps/dashboard && npm run format >/dev/null 2>&1; then \
		echo "✅ Dashboard formatting completed"; \
	else \
		echo "⚠️  Dashboard format command not configured"; \
	fi

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ .coverage htmlcov/
	cd apps/dashboard && rm -rf build/ node_modules/.cache/ || true
	@echo "✅ Cleanup complete"