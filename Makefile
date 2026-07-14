.PHONY: dev dev-backend dev-frontend test test-backend lint build up down seed clean

# ===========================
# Development
# ===========================

dev: ## Start all services via Docker Compose
	docker-compose up --build

dev-backend: ## Start backend only (local)
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend only (local)
	cd frontend && npm run dev

# ===========================
# Testing
# ===========================

test: test-backend ## Run all tests

test-backend: ## Run backend tests with coverage
	cd backend && pytest --cov=app --cov-report=term-missing -v

lint: ## Lint backend and frontend
	cd backend && python -m flake8 app/ --max-line-length=100
	cd frontend && npm run lint

# ===========================
# Docker
# ===========================

build: ## Build all Docker images
	docker-compose build --no-cache

up: ## Start all containers (detached)
	docker-compose up -d

down: ## Stop all containers
	docker-compose down

# ===========================
# Database
# ===========================

seed: ## Seed the database with demo data
	cd backend && python -m app.db.seed

migrate: ## Run database migrations
	cd backend && alembic upgrade head

migrate-new: ## Create a new migration
	cd backend && alembic revision --autogenerate -m "$(msg)"

# ===========================
# Cleanup
# ===========================

clean: ## Remove all build artifacts and containers
	docker-compose down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
