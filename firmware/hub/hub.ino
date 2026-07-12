#include <Arduino.h>
#include <comm_spi.h>
#include <msg_ctrl.h>
#include <key_matrix.h>

const uint8_t SLAVE_PIN = 9;


const uint8_t LEFT_MATRIX_ROWS = 5;
const uint8_t LEFT_MATRIX_COLS = 5;

uint8_t left_matrix[LEFT_MATRIX_ROWS];

void setup() {
  Serial.begin(9600);
  
  msg_ctrl_init();
  key_matrix_init(left_matrix, LEFT_MATRIX_ROWS);

  Serial.println("Hub initialized. Setting up SPI...");
  
  comm_spi_set_master();
  comm_spi_add_slave(SLAVE_PIN);
}

void loop() {
  msg_t *resp = NULL;
  static bool is_alive = false;

  comm_spi_start_transaction(SLAVE_PIN);

  for (uint8_t i = 0; i < 32; i++) {
    msg_ctrl_tick();
    resp = msg_ctrl_consume_response();
    if (resp != NULL) {
      break;
    }
    delayMicroseconds(30);
  }

  comm_spi_end_transaction(SLAVE_PIN);

  if (resp == NULL) {
    if (is_alive) {
      Serial.println("Error: Slave disconnected!");
      is_alive = false;
    }
  } else {
    if (!is_alive) {
      Serial.println("Slave on pin 9 is ALIVE!");
      is_alive = true;
    }

    if (resp->kind == MSG_KIND_KEYS) {
      bool any_pressed = false;
      uint8_t diff[LEFT_MATRIX_ROWS];

      key_matrix_diff(left_matrix, resp->buffer, diff, LEFT_MATRIX_ROWS);

      for (uint8_t r = 0; r < resp->size; r++) {
        for (uint8_t c = 0; c < LEFT_MATRIX_COLS; c++) {
          if (key_matrix_is_active(diff + r, c)) {
            if (key_matrix_is_active(resp->buffer + r, c)) {
              key_matrix_set_pressed(left_matrix + r, c);
              Serial.print("Key pressed at row ");
              Serial.print(r);
              Serial.print(", col ");
              Serial.println(c);
            } else {
              key_matrix_set_released(left_matrix + r, c);
              Serial.print("Key released at row ");
              Serial.print(r);
              Serial.print(", col ");
              Serial.println(c);
            }
          }
        }
      }
    } else if (resp->kind != MSG_KIND_HEARTBEAT) {
      Serial.print("Received message of kind: 0x");
      Serial.println(resp->kind, HEX);
    }
  }

  delay(10);
}
