BUILD_DIR ?= build
ARDUINO_CLI ?= arduino-cli

# Find all directories containing an .ino file
SKETCH_DIRS := $(dir $(wildcard */*.ino))
# Remove trailing slashes
SKETCH_DIRS := $(patsubst %/,%,$(SKETCH_DIRS))

# Define targets for each sketch directory
TARGETS := $(SKETCH_DIRS)

.PHONY: all clean $(TARGETS)

all: $(TARGETS)

# Rule to compile each sketch directory
$(TARGETS):
	@if [ ! -f $@/FQBN ]; then echo "Error: FQBN file missing in $@/"; exit 1; fi
	@echo "Compiling $@ for board $$(cat $@/FQBN)..."
	@if [ "$@" = "hub" ]; then \
		$(ARDUINO_CLI) compile --fqbn $$(cat $@/FQBN) --library $(CURDIR)/shared --build-property "compiler.cpp.extra_flags=-DIS_MASTER" --output-dir $(BUILD_DIR)/$@ $@; \
	else \
		$(ARDUINO_CLI) compile --fqbn $$(cat $@/FQBN) --library $(CURDIR)/shared --build-property "compiler.cpp.extra_flags=-DIS_SLAVE" --output-dir $(BUILD_DIR)/$@ $@; \
	fi

# Rule to upload a sketch
# Usage: make upload DIR=matrix_scaner PORT=/dev/ttyUSB0
PORT ?= /dev/ttyUSB0
.PHONY: upload
upload:
	@if [ -z "$(DIR)" ]; then echo "Error: DIR is not set. Usage: make upload DIR=<directory> [PORT=/dev/ttyUSB0]"; exit 1; fi
	@if [ ! -f $(DIR)/FQBN ]; then echo "Error: FQBN file missing in $(DIR)/"; exit 1; fi
	@echo "Uploading $(DIR) to $(PORT) for board $$(cat $(DIR)/FQBN)..."
	$(ARDUINO_CLI) upload -p $(PORT) --fqbn $$(cat $(DIR)/FQBN) --input-dir $(BUILD_DIR)/$(DIR)

# Rule to clean the build directory
clean:
	@echo "Cleaning build directory..."
	rm -rf $(BUILD_DIR)
