#include <Arduino.h>
#include <comm.h>
#include <msg_ctrl.h>
#include <key_matrix.h>
#include <stdint.h>
#include <SPI.h>

const uint8_t NUM_ROWS = 5;
const uint8_t NUM_COLS = 7;

unsigned long last_heard_from_master = 0;
unsigned long last_logged_timeout = 0;
const unsigned long MASTER_TIMEOUT_MS = 2000;
const unsigned long LOG_INTERVAL_MS = 2000;

const uint8_t rowPins[NUM_ROWS] = {A0, A1, A2, A3, A4};
const uint8_t colPins[NUM_COLS] = {3, 4, 5, 6, 7, 8, 9};

uint8_t matrix[NUM_ROWS];

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
  msg_ctrl_tick_all();
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
  msg_ctrl_init();
  comm_set_slave();

  Serial.begin(9600);

  while(!Serial) {
    ;
  }

  last_heard_from_master = millis();

  setupPins();
  key_matrix_init(matrix, NUM_ROWS);
}

void loop() {
  bool changed = false;

  for (uint8_t c = 0; c < NUM_COLS; c++) {
    digitalWrite(colPins[c], LOW);
    delayMicroseconds(10);

    for (uint8_t r = 0; r < NUM_ROWS; r++) {
      uint8_t is_pressed = digitalRead(rowPins[r]) == LOW;

      if (is_pressed != key_matrix_is_active(matrix + r, c)) {
        changed = true;

        debug_print_key_state(is_pressed, r, c);

        if (is_pressed) {
          key_matrix_set_pressed(matrix + r, c);
        } else {
          key_matrix_set_released(matrix + r, c);
        }
      }
    }

    digitalWrite(colPins[c], HIGH);
  }

  if (changed) {
    msg_t new_msg = {};

    new_msg.kind = MSG_KIND_KEYS;
    new_msg.size = NUM_ROWS;

    for(uint8_t i = 0; i < NUM_ROWS; i++) {
        new_msg.buffer[i] = matrix[i];
    }

    noInterrupts();
    msg_ctrl_produce(new_msg);
    interrupts();
  }

  while (true) {
    noInterrupts();
    msg_t *resp = msg_ctrl_consume_response();
    interrupts();

    if (resp == NULL) {
      break;
    }

    if (resp->kind == MSG_KIND_HEARTBEAT) {
      last_heard_from_master = millis();
    } else {
      Serial.print("Received non-heartbeat message of kind: 0x");
      Serial.println(resp->kind, HEX);
    }
  }



  if (millis() - last_heard_from_master > MASTER_TIMEOUT_MS) {
    if (millis() - last_logged_timeout > LOG_INTERVAL_MS) {
      Serial.println("Warning: Haven't heard from master");
      last_logged_timeout = millis();
    }
  }

  delay(20);
}
