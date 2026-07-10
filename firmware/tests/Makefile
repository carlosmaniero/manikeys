CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I.

TEST_SRCS = $(wildcard *.cpp)
TEST_EXEC = run_tests

all: $(TEST_EXEC)
	./$(TEST_EXEC)

$(TEST_EXEC): $(TEST_SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(TEST_EXEC)

.PHONY: all clean
