#include <Arduino.h>
#include <comm.h>
#include <msgs.h>
#include <key_matrix.h>
#include <stdint.h>

const uint8_t NUM_ROWS = 5;
const uint8_t NUM_COLS = 7;

const uint8_t rowPins[NUM_ROWS] = {A0, A1, A2, A3, A4};
const uint8_t colPins[NUM_COLS] = {3, 4, 5, 6, 7, 8, 9};

uint8_t matrix[NUM_COLS];

void debug_print_key_state(uint8_t is_pressed, uint8_t r, uint8_t c) {
  if (is_pressed) {
    Serial.print("Pressed [");
  } else {
    Serial.print("Released [");
  }
  Serial.print(r);
  Serial.print(", ");
  Serial.print(c);
  Serial.println("]");
}

void setupPins() {
  for (uint8_t r = 0; r < NUM_ROWS; r++) {
    pinMode(rowPins[r], INPUT_PULLUP);
  }

  for (uint8_t c = 0; c < NUM_COLS; c++) {
    pinMode(colPins[c], OUTPUT);
    digitalWrite(colPins[c], HIGH);
  }
}

void setup() {
  Serial.begin(9600);

  while(!Serial) {
    ;
  }

  setupPins();
  key_matrix_init(matrix, NUM_COLS);

  comm_set_slave();
  msg_send_heartbeat();
}

void loop() {
  msg_tick();

  bool changed = false;

  for (uint8_t c = 0; c < NUM_COLS; c++) {
    digitalWrite(colPins[c], LOW);
    delayMicroseconds(10);

    for (uint8_t r = 0; r < NUM_ROWS; r++) {
      uint8_t is_pressed = digitalRead(rowPins[r]) == LOW;

      if (is_pressed != key_matrix_is_pressed(matrix + c, r)) {
        changed = true;

        debug_print_key_state(is_pressed, r, c);

        if (is_pressed) {
          key_matrix_set_pressed(matrix + c, r);
        } else {
          key_matrix_set_released(matrix + c, r);
        }
      }
    }

    digitalWrite(colPins[c], HIGH);
  }

  if (changed) {
    msg_send_keys(matrix, NUM_COLS);
  }

  delay(20);
}
