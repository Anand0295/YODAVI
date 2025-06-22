# AI Vision Pro Makefile

.PHONY: help install dev test lint format clean run docker

help:
	@echo "AI Vision Pro - Available Commands:"
	@echo "  install     Install dependencies"
	@echo "  dev         Install development dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run code linting"
	@echo "  format      Format code"
	@echo "  clean       Clean build artifacts"
	@echo "  run         Run the application"
	@echo "  docker      Build and run Docker container"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black isort

test:
	python -m pytest tests/ -v --cov=src

lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/

run:
	python run.py

docker:
	docker build -t ai-vision-pro .
	docker run -p 3000:3000 ai-vision-pro

setup-samples:
	cd scripts && python download_samples.py

screenshots:
	cd scripts && python create_screenshots.py

demos:
	cd scripts && python create_demo_gifs.py