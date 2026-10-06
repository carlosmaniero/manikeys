SIMPLIFY ?= 0

.PHONY: build test lint render clean build_watch viewer

build: build/main.stl build/main.3mf \
	build/assembly/cad/main.stl \
	build/assembly/base_plate/cad/main.stl \
	build/assembly/base_plate/cad/hand.stl \
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


ifneq ($(filter clean,$(MAKECMDGOALS)),clean)
ALL_PY_FILES := $(shell find src -name "*.py")

build/deps.mk: $(ALL_PY_FILES)
	@mkdir -p build
	@uv run python scripts/scan_deps.py

-include build/deps.mk
endif

render: build/render.png build/render_back.png build/render_top.png build/render_side.png build/render_side_inv.png \
	build/render_angle0.png build/render_angle45.png build/render_angle90.png build/render_angle135.png \
	build/render_angle180.png build/render_angle225.png build/render_angle270.png build/render_angle315.png

PIN_HEADERS_STLS = build/components/female_pin_header/cad/female_pin_header_wire_holes_2.stl \
                   build/components/female_pin_header/cad/female_pin_header_wire_holes_3.stl \
                   build/components/female_pin_header/cad/female_pin_header_wire_holes_4.stl \
                   build/components/female_pin_header/cad/female_pin_header_wire_holes_5.stl \
                   build/components/female_pin_header/cad/female_pin_header_wire_holes_6.stl \
                   build/components/female_pin_header/cad/female_pin_header_wire_holes_7.stl \
                   build/components/female_pin_header/cad/female_pin_header_wire_holes_8.stl \
                   build/components/female_pin_header/cad/female_pin_header_wire_holes_9.stl

pin_headers: $(PIN_HEADERS_STLS)

build/components/female_pin_header/cad/female_pin_header_%.stl: src/components/female_pin_header/cad/female_pin_header_%.py src/components/female_pin_header/model.py src/components/female_pin_header/parameters.py
	@printf "STL\t%s\n" "$@"
	@mkdir -p $(dir $@)
	@+PYTHONPATH=src uv run python $< -o $@ $(DEPS_FLAG)
	@if [ "$(SIMPLIFY)" = "1" ]; then uv run python simplify.py -i $@ -o $@; fi

COMMA := ,
empty :=
space := $(empty) $(empty)
ALL_STLS = $(filter-out $(PIN_HEADERS_STLS),$(filter %.stl,$^))
ALL_PY_DEPS = $(filter-out $<,$(filter %.py,$^))
ALL_MODELS = $(ALL_PY_DEPS)
ALL_PARAMS =

STLS_FLAG = $(if $(strip $(ALL_STLS)),--stls $(subst $(space),$(COMMA),$(strip $(ALL_STLS))),)
PY_DEPS_FLAG = $(if $(strip $(ALL_PY_DEPS)),--py-deps $(subst $(space),$(COMMA),$(strip $(ALL_PY_DEPS))),)
PARAMS_FLAG = $(if $(strip $(ALL_PARAMS)),--parameters $(subst $(space),$(COMMA),$(strip $(ALL_PARAMS))),)
DEPS_FLAG = $(STLS_FLAG) $(PY_DEPS_FLAG)

build/%.3mf: src/%.py
	@mkdir -p $(dir $@)
	@+PYTHONPATH=src uv run python $< -o $@ $(DEPS_FLAG)

build/%.stl: src/%.py
	@printf "STL\t%s\n" "$@"
	@mkdir -p $(dir $@)
	@+PYTHONPATH=src uv run python $< -o $@ $(DEPS_FLAG)
	@if [ "$(SIMPLIFY)" = "1" ]; then uv run python simplify.py -i $@ -o $@; fi

F3D_RENDER_FLAGS = --resolution=2048,2048 --axis=false --grid=false --filename=false -q -a -t

build/%.png: build/%.3mf
	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=45 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=225 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-orthographic --camera-direction=0,0,-1 --camera-view-up=0,1,0 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-orthographic --camera-direction=0,-1,0 --camera-view-up=0,0,1 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-orthographic --camera-direction=0,1,0 --camera-view-up=0,0,1 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=0 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=45 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=90 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=135 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=180 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=225 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=270 $<

	f3d --output=$@ $(F3D_RENDER_FLAGS) --camera-elevation-angle=60 --camera-azimuth-angle=315 $<

test: build/assembly/cad/test_intersection.stl
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

viewer:
	uv run python viewer/server.py

clean:
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
