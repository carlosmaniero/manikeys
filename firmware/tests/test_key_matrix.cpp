#include <iostream>
#include <cassert>
#include <stdint.h>

#include "../shared/src/key_matrix.h"

#include "tests.h"

TEST_START(test_key_matrix_init)
  uint8_t size = 5;
  uint8_t matrix[size];
  
  key_matrix_init(matrix, size);
  
  for (int i = 0; i < size - 1; i++) {
      assert(matrix[i] == 1);
  }
  
  assert(matrix[size - 1] == 0);
TEST_END

TEST_START(test_key_pressed_released)
  uint8_t size = 5;
  uint8_t matrix[size];

  key_matrix_init(matrix, size);

  assert(key_matrix_is_active(&matrix[1], 2) == 0);

  key_matrix_set_pressed(&matrix[1], 2);

  assert(key_matrix_is_active(&matrix[1], 0) == 0);
  assert(key_matrix_is_active(&matrix[1], 1) == 0);
  assert(key_matrix_is_active(&matrix[1], 2));
  assert(key_matrix_is_active(&matrix[1], 3) == 0);
  assert(key_matrix_is_active(&matrix[1], 4) == 0);
  assert(key_matrix_is_active(&matrix[1], 5) == 0);
  assert(key_matrix_is_active(&matrix[1], 6) == 0);

  key_matrix_set_released(&matrix[1], 2);

  assert(key_matrix_is_active(&matrix[1], 2) == 0);
TEST_END

TEST_START(test_key_matrix_next)
  uint8_t size = 3;
  uint8_t matrix[size];

  key_matrix_init(matrix, size);

  uint8_t* current = matrix;
  
  current = key_matrix_next(current);
  assert(current == &matrix[1]);
  
  current = key_matrix_next(current);
  assert(current == &matrix[2]);
  
  current = key_matrix_next(current);
  assert(current == 0);
TEST_END

TEST_START(test_key_matrix_diff)
  uint8_t size = 3;
  uint8_t prev[size];
  uint8_t curr[size];
  uint8_t diff[size];

  // Test 1: Key Pressed
  key_matrix_init(prev, size);
  key_matrix_init(curr, size);
  key_matrix_init(diff, size);
  key_matrix_set_pressed(&curr[1], 2); // Press index 1, bit 2 in curr

  key_matrix_diff(prev, curr, diff, size);
  assert(key_matrix_is_active(&diff[1], 2) == 1);
  assert(key_matrix_is_active(&diff[1], 1) == 0);

  // Test 2: Key Released
  key_matrix_init(prev, size);
  key_matrix_init(curr, size);
  key_matrix_init(diff, size);
  key_matrix_set_pressed(&prev[1], 2); // prev has it pressed, curr has it released

  key_matrix_diff(prev, curr, diff, size);
  assert(key_matrix_is_active(&diff[1], 2) == 1);
TEST_END

int main() {
  std::cout << "Running tests..." << std::endl;

  test_key_matrix_init();
  test_key_pressed_released();
  test_key_matrix_next();
  test_key_matrix_diff();

  std::cout << "All tests passed successfully!" << std::endl;

  return 0;
}
