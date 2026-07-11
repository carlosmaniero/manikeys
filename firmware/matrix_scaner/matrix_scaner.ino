#include <Arduino.h>
#include <comm.h>
#include <msgs.h>
#include <key_matrix.h>
#include <stdint.h>
#include <SPI.h>

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

ISR(SPI_STC_vect) {
  msgs_tick();
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
  msgs_init();
  comm_set_slave();

  Serial.begin(9600);

  while(!Serial) {
    ;
  }

  setupPins();
  key_matrix_init(matrix, NUM_COLS);
}

void loop() {
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
    msgs_msg_t new_msg = {};
    new_msg.kind = MSG_KIND_KEYS;
    new_msg.size = NUM_COLS;
    for(uint8_t i = 0; i < NUM_COLS; i++) {
        new_msg.buffer[i] = matrix[i];
    }
    msgs_produce(new_msg);
  }

  delay(20);
}
