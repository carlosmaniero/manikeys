#include "key_matrix.h"

void key_matrix_init(uint8_t* matrix, uint8_t size) {
  for (uint8_t i = 0; i < size - 1; i++) {
    matrix[i] = 1;
  }
  matrix[size - 1] = 0;
}

uint8_t _key_matrix_mask(uint8_t bit_index) {
  return 1 << (bit_index + 1);
}

void key_matrix_set_pressed(uint8_t* matrix, uint8_t bit_index) {
  *matrix |= _key_matrix_mask(bit_index);
}

void key_matrix_set_released(uint8_t* matrix, uint8_t bit_index) {
  *matrix &= ~(_key_matrix_mask(bit_index));
}

uint8_t key_matrix_is_pressed(uint8_t* matrix, uint8_t bit_index) {
  return (*matrix & _key_matrix_mask(bit_index)) ? 1 : 0;
}

uint8_t* key_matrix_next(uint8_t* matrix) {
  if (*matrix & 1) {
    return matrix + 1;
  }
  return 0;
}
