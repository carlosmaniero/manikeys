.PHONY: build test lint render clean sphere build_watch

build: build/main.stl build/main.3mf

build_watch:
	@target="$(filter-out $@,$(MAKECMDGOALS))"; \
	if [ -z "$$target" ]; then \
		echo "Error: Please specify a target, e.g., make build_watch build/main.stl"; \
		exit 1; \
	fi; \
	echo "Watching src/ for changes to build $$target..."; \
	uv run watchmedo shell-command \
		--patterns="*.py" \
		--ignore-patterns="*__pycache__*" \
		--recursive \
		--drop \
		--ignore-directories \
		--command="rm -f $$target && make $$target" \
		src/


sphere: build/sphere.stl build/sphere.png

render: build/main.png build/main_back.png build/main_top.png build/main_side.png build/main_side_inv.png

build/main.stl: src/main.py build/cad/body.stl build/cad/cap_grid.stl build/cad/cap_hole_grid.stl build/cad/body_numpy.stl
build/cad/cap_grid.stl: src/cad/cap_grid.py build/cad/cap.stl
build/cad/cap_hole_grid.stl: src/cad/cap_hole_grid.py build/cad/cap_hole.stl

build/%.3mf: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run python $< -o $@

build/%.stl: src/%.py
	mkdir -p $(dir $@)
	PYTHONPATH=src uv run python $< -o $@
	uv run python simplify.py -i $@ -o $@

build_with_pythonscad:
	@if [ "$(suffix $(FILE))" = ".stl" ]; then \
		$(MAKE) _pythonscad_stl FILE=$(FILE); \
	elif [ "$(suffix $(FILE))" = ".3mf" ]; then \
		$(MAKE) _pythonscad_3mf FILE=$(FILE); \
	else \
		$(MAKE) _pythonscad_other FILE=$(FILE); \
	fi

_pythonscad_stl:
	mkdir -p $(dir $(FILE))
	PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $(shell find src -name "$(notdir $(basename $(FILE))).py") -o $(FILE) --export-format binstl
	uv run python simplify.py -i $(FILE) -o $(FILE)

_pythonscad_3mf:
	mkdir -p $(dir $(FILE))
	PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $(shell find src -name "$(notdir $(basename $(FILE))).py") -o $(FILE)

_pythonscad_other:
	mkdir -p $(dir $(FILE))
	PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $(shell find src -name "$(notdir $(basename $(FILE))).py") -o $(FILE)


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

# Catch-all to allow positional arguments for build_watch
%:
	@:
