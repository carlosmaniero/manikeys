#include <iostream>
#include <cassert>
#include <stdint.h>

#include "../shared/src/key_matrix.h"

#include "tests.h"

TEST_START(test_key_matrix_init)
  uint8_t cols = 5;
  uint8_t matrix[cols];
  
  key_matrix_init(matrix, cols);
  
  for (int i = 0; i < cols - 1; i++) {
      assert(matrix[i] == 1);
  }
  
  assert(matrix[cols - 1] == 0);
TEST_END

TEST_START(test_key_pressed_released)
  uint8_t cols = 5;
  uint8_t matrix[cols];

  key_matrix_init(matrix, cols);

  assert(key_matrix_is_pressed(&matrix[1], 2) == 0);

  key_matrix_set_pressed(&matrix[1], 2);

  assert(key_matrix_is_pressed(&matrix[1], 0) == 0);
  assert(key_matrix_is_pressed(&matrix[1], 1) == 0);
  assert(key_matrix_is_pressed(&matrix[1], 2));
  assert(key_matrix_is_pressed(&matrix[1], 3) == 0);
  assert(key_matrix_is_pressed(&matrix[1], 4) == 0);
  assert(key_matrix_is_pressed(&matrix[1], 5) == 0);
  assert(key_matrix_is_pressed(&matrix[1], 6) == 0);

  key_matrix_set_released(&matrix[1], 2);

  assert(key_matrix_is_pressed(&matrix[1], 2) == 0);
TEST_END

TEST_START(test_key_matrix_next)
  uint8_t cols = 3;
  uint8_t matrix[cols];

  key_matrix_init(matrix, cols);

  uint8_t* current = matrix;
  
  current = key_matrix_next(current);
  assert(current == &matrix[1]);
  
  current = key_matrix_next(current);
  assert(current == &matrix[2]);
  
  current = key_matrix_next(current);
  assert(current == 0);
TEST_END

int main() {
  std::cout << "Running tests..." << std::endl;

  test_key_matrix_init();
  test_key_pressed_released();
  test_key_matrix_next();

  std::cout << "All tests passed successfully!" << std::endl;

  return 0;
}
