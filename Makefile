SIMPLIFY ?= 1

.PHONY: build test lint render clean sphere build_watch

build: build/main.stl build/main.3mf build/main.wrl \
	build/cad/full_keyboard_main.stl \
	build/cad/full_keyboard_hand.stl \
	build/cad/full_keyboard_side.stl

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


sphere: build/sphere.wrl build/sphere.png

render: build/render.png build/render_back.png build/render_top.png build/render_side.png build/render_side_inv.png \
	build/render_angle0.png build/render_angle45.png build/render_angle90.png build/render_angle135.png \
	build/render_angle180.png build/render_angle225.png build/render_angle270.png build/render_angle315.png

build/sphere.3mf: src/openscad_ext/demo.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@

build/sphere.wrl: src/openscad_ext/demo.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@

build/main.stl build/main.3mf build/main.wrl: src/main.py build/full_keyboard.stl build/cad/body_bottom.stl build/cad/socket_adapter_grid.stl build/cad/cap_top_grid.stl
build/render.3mf: src/render.py build/main.3mf
build/full_keyboard.stl build/full_keyboard.3mf build/full_keyboard.wrl: src/full_keyboard.py build/cad/body.stl build/cad/body_inner_sections.stl build/cad/body_screw_placement.stl build/cad/socket_placement_shell.stl build/cad/body_screw_mask.stl build/cad/body_screw_hole.stl build/cad/logo.stl build/cad/cap_grid.stl build/cad/cap_hole_grid.stl build/cad/cap_thumb.stl build/cad/cap_thumb_hole.stl build/cad/cable_path.stl build/cad/connectors/rj11_mask.stl build/cad/connectors/rj11_adapter_trimmed.stl
build/cad/cable_path.stl: src/cad/cable_path.py
build/cad/logo.stl: src/cad/logo.py dist/mani-logo.stl
build/cad/body_screw_placement.stl: src/cad/body_screw_placement.py build/cad/body.stl
build/cad/body_screw_mask.stl: src/cad/body_screw_mask.py
build/cad/body_screw_hole.stl: src/cad/body_screw_hole.py
build/cad/body_bottom.stl: src/cad/body_bottom.py build/cad/body.stl
build/cad/socket_placement_shell.stl: src/cad/socket_placement_shell.py build/cad/socket_placement.stl build/cad/socket_placement_inner_sections.stl
build/cad/body_inner_sections.stl: src/cad/body_inner_sections.py build/cad/body_inner.stl
build/cad/socket_placement_inner_sections.stl: src/cad/socket_placement_inner_sections.py build/cad/socket_placement_inner.stl
build/cad/cap_grid.stl: src/cad/cap_grid.py build/cad/cap.stl
build/cad/cap_hole_grid.stl: src/cad/cap_hole_grid.py build/cad/cap_hole.stl
build/cad/cap_thumb.stl: src/cad/cap_thumb.py build/cad/cap.stl
build/cad/cap_thumb_hole.stl: src/cad/cap_thumb_hole.py build/cad/cap_hole.stl
build/cad/socket_adapter_grid.stl: src/cad/socket_adapter_grid.py build/cad/socket_adapter.stl

build/cad/connectors/rj11_adapter_trimmed.stl: src/cad/connectors/rj11_adapter_trimmed.py build/cad/connectors/rj11_adapter.stl build/cad/body.stl

build/cad/full_keyboard_main.stl: src/cad/full_keyboard_main.py build/full_keyboard.stl
build/cad/full_keyboard_hand.stl: src/cad/full_keyboard_hand.py build/full_keyboard.stl
build/cad/full_keyboard_side.stl: src/cad/full_keyboard_side.py build/full_keyboard.stl

build/%.wrl: src/%.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@

build/%.3mf: src/%.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@

build/%.stl: src/%.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@
	@if [ "$(SIMPLIFY)" = "1" ]; then uv run python simplify.py -i $@ -o $@; fi

build/%.stl: src/%.scad
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $< -o $@ --export-format binstl
	@if [ "$(SIMPLIFY)" = "1" ]; then uv run python simplify.py -i $@ -o $@; fi

build_with_pythonscad:
	@if [ "$(suffix $(FILE))" = ".stl" ]; then \
		$(MAKE) _pythonscad_stl FILE=$(FILE); \
	elif [ "$(suffix $(FILE))" = ".3mf" ]; then \
		$(MAKE) _pythonscad_3mf FILE=$(FILE); \
	elif [ "$(suffix $(FILE))" = ".wrl" ]; then \
		$(MAKE) _pythonscad_wrl FILE=$(FILE); \
	else \
		$(MAKE) _pythonscad_other FILE=$(FILE); \
	fi

_pythonscad_stl:
	mkdir -p $(dir $(FILE))
	PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $(patsubst build/%,src/%,$(basename $(FILE)).py) -o $(FILE) --export-format binstl
	@if [ "$(SIMPLIFY)" = "1" ]; then uv run python simplify.py -i $(FILE) -o $(FILE); fi

_pythonscad_3mf:
	mkdir -p $(dir $(FILE))
	PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $(patsubst build/%,src/%,$(basename $(FILE)).py) -o $(FILE) -O export-3mf/material-type=color

_pythonscad_wrl:
	mkdir -p $(dir $(FILE))
	PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $(patsubst build/%,src/%,$(basename $(FILE)).py) -o $(FILE)

_pythonscad_other:
	mkdir -p $(dir $(FILE))
	PYTHONPATH=src uv run pythonscad --backend Manifold --trust-python $(patsubst build/%,src/%,$(basename $(FILE)).py) -o $(FILE)



PYTHONSCAD_RENDER_FLAGS = --render --imgsize=2048,2048 --viewall --autocenter

build/%.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,45,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_back.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,225,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_top.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --projection=o --camera=0,0,0,0,0,0,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_side.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --projection=o --camera=0,0,0,90,0,0,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_side_inv.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --projection=o --camera=0,0,0,90,0,180,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle0.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,0,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle45.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,45,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle90.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,90,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle135.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,135,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle180.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,180,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle225.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,225,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle270.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,270,0 -D 'import("'$(abspath $<)'");' /dev/null

build/%_angle315.png: build/%.3mf
	pythonscad -o $@ $(PYTHONSCAD_RENDER_FLAGS) --camera=0,0,0,60,0,315,0 -D 'import("'$(abspath $<)'");' /dev/null

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
