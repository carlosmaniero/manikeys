#include <stdint.h>

void key_matrix_init(uint8_t* matrix, uint8_t cols) {
  for (uint8_t i = 0; i < cols - 1; i++) {
    matrix[i] = 1;
  }
  matrix[cols - 1] = 0;
}

uint8_t _key_matrix_mask(uint8_t row) {
  return 1 << (row + 1);
}

void key_matrix_set_pressed(uint8_t* matrix, uint8_t row) {
  *matrix |= _key_matrix_mask(row);
}

void key_matrix_set_released(uint8_t* matrix, uint8_t row) {
  *matrix &= ~(_key_matrix_mask(row));
}

uint8_t key_matrix_is_pressed(uint8_t* matrix, uint8_t row) {
  return *matrix & _key_matrix_mask(row);
}

uint8_t* key_matrix_next(uint8_t* matrix) {
  if (*matrix & 1) {
    return matrix + 1;
  }
  return 0;
}
