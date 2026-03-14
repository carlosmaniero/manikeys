.PHONY: build test lint render clean sphere

build: build/main.stl build/main.3mf

sphere: build/sphere.stl build/sphere.png

render: build/main.png build/main_back.png build/main_top.png build/main_side.png build/main_side_inv.png

build/%.stl: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run python $< -o $@

build/%.3mf: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run python $< -o $@

F3D_FLAGS = --resolution 2048,2048 --anti-aliasing=ssaa --no-config --axis=0 --grid=0 --up +Z --no-background

build/%.png: build/%.stl
	f3d $< $(F3D_FLAGS) --output $@ --camera-azimuth-angle 45 --camera-elevation-angle 30

build/%_back.png: build/%.stl
	f3d $< $(F3D_FLAGS) --output $@ --camera-azimuth-angle 225 --camera-elevation-angle 30

build/%_top.png: build/%.stl
	f3d $< $(F3D_FLAGS) --output $@ --camera-orthographic --camera-direction 0,0,-1 --camera-view-up 0,1,0

build/%_side.png: build/%.stl
	f3d $< $(F3D_FLAGS) --output $@ --camera-orthographic --camera-direction 0,-1,0 --camera-view-up 0,0,1

build/%_side_inv.png: build/%.stl
	f3d $< $(F3D_FLAGS) --output $@ --camera-orthographic --camera-direction 0,1,0 --camera-view-up 0,0,1

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

clean:
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
