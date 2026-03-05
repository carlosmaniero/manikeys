.PHONY: build test lint render clean

build: build/main.stl build/main.3mf

render: build/main.png build/main_top.png build/main_side.png

build/%.stl: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run pythonscad $< --trust-python -o $@

build/%.3mf: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run pythonscad $< --trust-python -o $@

build/%.png: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run xvfb-run --auto-servernum pythonscad $< --trust-python --colorscheme "Metallic" --imgsize 2048,2048 --render --viewall -o $@

build/%_top.png: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run xvfb-run --auto-servernum pythonscad $< --trust-python --colorscheme "Metallic" --imgsize 2048,2048 --render --viewall --camera 0,0,0,0,0,0,0 -o $@

build/%_side.png: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run xvfb-run --auto-servernum pythonscad $< --trust-python --colorscheme "Metallic" --imgsize 2048,2048 --render --viewall --camera 0,0,0,90,0,90,0 -o $@

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

clean:
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
