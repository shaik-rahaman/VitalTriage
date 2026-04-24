# VitalTriage Backend - Makefile
# Quick commands for common tasks

.PHONY: help install setup run dev test demo clean docker-up docker-down

help:
	@echo "🏥 VitalTriage Backend - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install      - Install dependencies"
	@echo "  make setup        - Full setup (venv + dependencies + .env)"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Run development server with auto-reload"
	@echo "  make run          - Run production server"
	@echo ""
	@echo "Database:"
	@echo "  make demo         - Load demo patients"
	@echo "  make docker-up    - Start MongoDB in Docker"
	@echo "  make docker-down  - Stop MongoDB in Docker"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Run linting"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean        - Clean cache files"
	@echo "  make requirements - Freeze requirements"
	@echo ""

# Installation
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

setup:
	@echo "🔧 Running full setup..."
	@bash setup.sh

# Development
dev:
	@echo "🚀 Starting development server..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run:
	@echo "🚀 Starting production server..."
	uvicorn app.main:app --host 0.0.0.0 --port 8000

# Database
demo:
	@echo "📊 Loading demo patients..."
	python demo_data.py

docker-up:
	@echo "🐳 Starting MongoDB container..."
	docker-compose up -d
	@echo "✓ MongoDB started on localhost:27017"

docker-down:
	@echo "🛑 Stopping MongoDB container..."
	docker-compose down
	@echo "✓ MongoDB stopped"

# Testing
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ --cov=app --cov-report=html
	@echo "✓ Coverage report generated in htmlcov/index.html"

lint:
	@echo "🔍 Running linting..."
	python -m pylint app/

# Utilities
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cache cleaned"

requirements:
	@echo "📝 Freezing requirements..."
	pip freeze > requirements.txt
	@echo "✓ Requirements frozen"
