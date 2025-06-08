# Rotator CLI Makefile

.PHONY: install install-dev test lint format clean build publish help

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install the package"
	@echo "  install-dev - Install with development dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build distribution packages"
	@echo "  publish     - Publish to PyPI (requires credentials)"

# Installation
install:
	uv pip install .

install-dev:
	uv sync --dev

# Development
test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

# Build and publish
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	uv build

publish: build
	uv publish

# Homebrew formula generation
homebrew-formula:
	@echo "Generate Homebrew formula with actual SHA256 values after creating a release"
	@echo "Formula template is in rotator_cli/homebrew_formula.rb"