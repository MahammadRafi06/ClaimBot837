.PHONY: install test lint format clean docs run

# Development setup
install:
	pip install -r requirements.txt

# Testing
test:
	pytest tests/ --cov=app --cov-report=term-missing

# Code quality
lint:
	flake8 app/
	pylint app/
	mypy app/

format:
	black app/
	isort app/

# Documentation
docs:
	sphinx-build -b html docs/source/ docs/build/

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf docs/build/

# Run application
run:
	python -m flask run --host=0.0.0.0 --port=5000

# Docker commands
docker-build:
	docker build -t claimbot837 .

docker-run:
	docker run -p 5000:5000 claimbot837

# Database
db-init:
	python -m app.db.init

db-migrate:
	python -m app.db.migrate

# Help
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test      - Run tests with coverage"
	@echo "  make lint      - Run linters"
	@echo "  make format    - Format code"
	@echo "  make clean     - Clean build artifacts"
	@echo "  make docs      - Build documentation"
	@echo "  make run       - Run the application"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make db-init     - Initialize database"
	@echo "  make db-migrate  - Run database migrations" 