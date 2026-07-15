CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I. -I../shared/src
BUILD_DIR = build

MOCK_SRCS = comm_mock.cpp
SHARED_SRCS = ../shared/src/key_matrix.cpp ../shared/src/msg.cpp ../shared/src/queue.cpp ../shared/src/msg_ctrl.cpp

TEST_EXECS = $(BUILD_DIR)/test_key_matrix $(BUILD_DIR)/test_msgs_master $(BUILD_DIR)/test_msgs_slave

all: $(BUILD_DIR) $(TEST_EXECS) run_all

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Compile key_matrix tests
$(BUILD_DIR)/test_key_matrix: test_key_matrix.cpp $(MOCK_SRCS) $(SHARED_SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compile msgs tests for master configuration
$(BUILD_DIR)/test_msgs_master: test_msgs_master.cpp $(MOCK_SRCS) $(SHARED_SRCS)
	$(CXX) $(CXXFLAGS) -DIS_MASTER -o $@ $^

# Compile msgs tests for slave configuration
$(BUILD_DIR)/test_msgs_slave: test_msgs_slave.cpp $(MOCK_SRCS) $(SHARED_SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^

run_all: $(TEST_EXECS)
	@for test in $(TEST_EXECS); do \
		echo "\n--- Running $$test ---"; \
		$$test; \
	done

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean run_all
