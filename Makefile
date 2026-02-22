.PHONY: build test lint clean

build:
	mkdir -p build
	pythonscad main.py --trust-python -o build/keyboard.stl

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

clean:
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
