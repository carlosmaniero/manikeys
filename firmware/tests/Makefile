CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I. -I../shared/src
BUILD_DIR = build

TEST_SRCS = $(wildcard test_*.cpp)
TEST_EXECS = $(patsubst %.cpp,$(BUILD_DIR)/%,$(TEST_SRCS))
MOCK_SRCS = $(filter-out $(TEST_SRCS), $(wildcard *.cpp))

all: $(BUILD_DIR) $(TEST_EXECS) run_all

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Compile each test with the mocks
$(BUILD_DIR)/%: %.cpp $(MOCK_SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^

run_all: $(TEST_EXECS)
	@for test in $(TEST_EXECS); do \
		echo "\n--- Running $$test ---"; \
		$$test; \
	done

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean run_all
