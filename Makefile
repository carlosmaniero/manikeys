SIMPLIFY ?= 1

.PHONY: build test lint render clean build_watch viewer

build: build/main.stl build/main.3mf \
	build/assembly/cad/main.stl \
	build/assembly/base_plate/cad/main.stl \
	build/assembly/cad/supports/main.stl \
	build/assembly/cad/hand.stl \
	build/assembly/cad/supports/hand.stl \
	build/assembly/cad/side.stl

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


render: build/render.png build/render_back.png build/render_top.png build/render_side.png build/render_side_inv.png \
	build/render_angle0.png build/render_angle45.png build/render_angle90.png build/render_angle135.png \
	build/render_angle180.png build/render_angle225.png build/render_angle270.png build/render_angle315.png

build/main.stl build/main.3mf: src/main.py build/assembly/cad/full_keyboard.stl build/assembly/base_plate/cad/base_plate.stl build/switches/socket/mount/cad/shell.stl build/switches/socket/cad/hot_swap_grid.stl build/switches/cad/keycap_grid.stl build/connectors/rj11/cad/rj11.stl build/connectors/rj11/cad/adapter_trimmed.stl
build/render.3mf: src/render.py build/main.3mf
build/assembly/cad/full_keyboard.stl build/full_keyboard.3mf: src/assembly/cad/full_keyboard.py build/structure/body/shape.stl build/structure/body/cad/body_cavity_sections.stl build/structure/body/screws/cad/placement.stl build/structure/body/screws/cad/hole.stl build/cad/logo.stl build/switches/cad/switch_hole_decorator_grid.stl build/switches/cad/switch_hole_grid.stl build/switches/cad/switch_decorator_thumb_grid.stl build/switches/cad/switch_thumb_hole.stl build/connectors/pogo/cad/cable_path.stl build/connectors/rj11/cad/masks/rj11.stl build/connectors/rj11/cad/placement.stl build/connectors/usbc/cad/masks/usbc.stl build/connectors/usbc/cad/adapter_trimmed.stl build/connectors/magnet/cad/snap.stl build/components/light_indicator/cad/masks/body.stl build/components/light_indicator/cad/panel_frame.stl build/components/oled_096/cad/masks/body.stl build/components/oled_096/cad/placement.stl build/connectors/rj45/cad/masks/body.stl build/connectors/rj45/cad/placement.stl
build/connectors/magnet/cad/snap.stl: src/connectors/magnet/cad/snap.py
build/cad/magnet_demo.stl: src/cad/magnet_demo.py
build/connectors/pogo/cad/cable_path.stl: src/connectors/pogo/cad/cable_path.py build/connectors/pogo/cad/pogo_pin_adapter.stl
build/cad/logo.stl: src/cad/logo.py dist/mani-logo.stl
build/structure/body/screws/cad/placement.stl: src/structure/body/screws/cad/placement.py build/structure/body/shape.stl
build/switches/socket/mount/cad/screw_clearance.stl: src/switches/socket/mount/cad/screw_clearance.py
build/structure/body/screws/cad/hole.stl: src/structure/body/screws/cad/hole.py
build/assembly/base_plate/cad/base_plate.stl: src/assembly/base_plate/cad/base_plate.py build/components/arduino_nano_case/cad/case.stl build/components/arduino_pro_micro_case/cad/housing.stl
build/switches/socket/mount/cad/shell.stl: src/switches/socket/mount/cad/shell.py build/switches/socket/mount/cad/body.stl build/switches/socket/mount/cad/cavity_sections.stl build/connectors/rj45/cad/masks/placement.stl build/connectors/usbc/cad/masks/placement.stl build/switches/socket/mount/cad/screw_clearance.stl build/switches/cad/switch_hole_decorator_shell_grid.stl build/switches/cad/switch_hole_grid.stl build/switches/cad/switch_thumb_hole.stl build/connectors/pogo/cad/cable_path.stl build/components/light_indicator/cad/masks/body_shell.stl build/components/oled_096/cad/masks/shell.stl
build/structure/body/cad/body_cavity_sections.stl: src/structure/body/cad/body_cavity_sections.py build/structure/body/cad/body_cavity.stl
build/switches/socket/mount/cad/cavity_sections.stl: src/switches/socket/mount/cad/cavity_sections.py build/switches/socket/mount/cad/cavity.stl
build/switches/cad/switch_hole_decorator.stl: src/switches/cad/switch_hole_decorator.py build/switches/cad/switch_hole.stl
build/switches/cad/switch_hole_decorator_grid.stl: src/switches/cad/switch_hole_decorator_grid.py build/switches/cad/switch_hole_decorator.stl
build/switches/cad/switch_hole_decorator_shell.stl: src/switches/cad/switch_hole_decorator_shell.py build/switches/socket/cad/hot_swap_placement_mask.stl build/switches/cad/switch_hole.stl
build/switches/cad/switch_hole_decorator_shell_grid.stl: src/switches/cad/switch_hole_decorator_shell_grid.py build/switches/cad/switch_hole_decorator_shell.stl
build/switches/cad/switch_hole_grid.stl: src/switches/cad/switch_hole_grid.py build/switches/cad/switch_hole.stl
build/switches/cad/switch_decorator_thumb_grid.stl: src/switches/cad/switch_decorator_thumb_grid.py build/switches/cad/switch_hole_decorator.stl
build/switches/cad/switch_thumb_hole.stl: src/switches/cad/switch_thumb_hole.py build/switches/cad/switch_hole.stl
build/switches/socket/cad/hot_swap_grid.stl: src/switches/socket/cad/hot_swap_grid.py build/switches/socket/cad/hot_swap.stl
build/switches/socket/cad/hot_swap_placement_mask.stl: src/switches/socket/cad/hot_swap_placement_mask.py
build/components/oled_096/cad/placement.stl: src/components/oled_096/cad/placement.py build/components/oled_096/cad/oled.stl
build/components/oled_096/cad/masks/body.stl: src/components/oled_096/cad/masks/body.py
build/components/oled_096/cad/masks/shell.stl: src/components/oled_096/cad/masks/shell.py

build/connectors/rj11/cad/adapter_trimmed.stl: src/connectors/rj11/cad/adapter_trimmed.py build/connectors/rj11/cad/adapter.stl build/structure/body/shape.stl
build/connectors/rj11/cad/placement.stl: src/connectors/rj11/cad/placement.py build/structure/body/shape.stl
build/connectors/usbc/cad/adapter.stl: src/connectors/usbc/cad/adapter.py build/connectors/usbc/cad/masks/connector.stl
build/connectors/usbc/cad/adapter_trimmed.stl: src/connectors/usbc/cad/adapter_trimmed.py build/connectors/usbc/cad/adapter.stl build/structure/body/shape.stl
build/connectors/usbc/cad/masks/usbc.stl: src/connectors/usbc/cad/masks/usbc.py build/connectors/usbc/cad/masks/connector.stl
build/connectors/usbc/cad/masks/placement.stl: src/connectors/usbc/cad/masks/placement.py

build/connectors/rj45/cad/placement.stl: src/connectors/rj45/cad/placement.py build/connectors/rj45/cad/adapter_front.stl build/structure/body/shape.stl
build/connectors/pogo/cad/pogo_pin_mask.stl: src/connectors/pogo/cad/pogo_pin_mask.py
build/connectors/pogo/cad/pogo_pin_adapter.stl: src/connectors/pogo/cad/pogo_pin_adapter.py build/connectors/pogo/cad/pogo_pin_mask.stl

build/assembly/cad/main.stl: src/assembly/cad/main.py build/assembly/cad/full_keyboard.stl
build/assembly/base_plate/cad/main.stl: src/assembly/base_plate/cad/main.py build/assembly/base_plate/cad/base_plate.stl
build/assembly/cad/supports/main.stl: src/assembly/cad/supports/main.py build/assembly/cad/main.stl build/structure/body/cad/body_cavity.stl build/structure/body/screws/cad/hole.stl
build/assembly/cad/hand.stl: src/assembly/cad/hand.py build/assembly/cad/full_keyboard.stl
build/assembly/cad/supports/hand.stl: src/assembly/cad/supports/hand.py build/assembly/cad/hand.stl build/structure/body/cad/body_cavity.stl build/structure/body/screws/cad/hole.stl
build/assembly/cad/side.stl: src/assembly/cad/side.py build/assembly/cad/full_keyboard.stl

build/structure/%/shape.3mf: src/structure/%/cad/shape.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@

build/structure/%/shape.stl: src/structure/%/cad/shape.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@
	@if [ "$(SIMPLIFY)" = "1" ]; then uv run python simplify.py -i $@ -o $@; fi

build/%.3mf: src/%.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@

build/%.stl: src/%.py
	mkdir -p $(dir $@)
	+PYTHONPATH=src uv run python $< -o $@
	@if [ "$(SIMPLIFY)" = "1" ]; then uv run python simplify.py -i $@ -o $@; fi





F3D_RENDER_FLAGS = --resolution=2048,2048 --axis=false --grid=false --filename=false -q -a -t

build/%.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=45 $<

build/%_back.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=225 $<

build/%_top.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-orthographic --camera-direction=0,0,-1 --camera-view-up=0,1,0 $<

build/%_side.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-orthographic --camera-direction=0,-1,0 --camera-view-up=0,0,1 $<

build/%_side_inv.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-orthographic --camera-direction=0,1,0 --camera-view-up=0,0,1 $<

build/%_angle0.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=0 $<

build/%_angle45.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=45 $<

build/%_angle90.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=90 $<

build/%_angle135.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=135 $<

build/%_angle180.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=180 $<

build/%_angle225.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=225 $<

build/%_angle270.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=270 $<

build/%_angle315.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=315 $<

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

viewer:
	uv run python viewer/server.py

clean:
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Catch-all to allow positional arguments for build_watch
%:
	@:
