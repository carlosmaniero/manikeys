.PHONY: build test lint render clean

build:
	mkdir -p build
	uv run pythonscad src/main.py --trust-python -o build/keyboard.stl

render:
	mkdir -p build
	uv run xvfb-run --auto-servernum pythonscad src/main.py --trust-python --colorscheme "Tomorrow Night" --imgsize 2048,2048 --render -o build/keyboard.png

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

clean:
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
