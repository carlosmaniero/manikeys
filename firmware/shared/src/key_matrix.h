#ifndef KEY_MATRIX_H
#define KEY_MATRIX_H

#include <stdint.h>

void key_matrix_init(uint8_t* matrix, uint8_t size);
uint8_t _key_matrix_mask(uint8_t bit_index);
void key_matrix_set_pressed(uint8_t* matrix, uint8_t bit_index);
void key_matrix_set_released(uint8_t* matrix, uint8_t bit_index);
uint8_t key_matrix_is_active(uint8_t* matrix, uint8_t bit_index);
uint8_t* key_matrix_next(uint8_t* matrix);
void key_matrix_diff(uint8_t* prev, uint8_t* curr, uint8_t* diff, uint8_t size);

#endif // KEY_MATRIX_H
