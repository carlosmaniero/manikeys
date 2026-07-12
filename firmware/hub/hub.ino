#include <Arduino.h>
#include <comm_spi.h>
#include <msg_ctrl.h>
#include <key_matrix.h>

const uint8_t SLAVE_PIN = 9;

void setup() {
  Serial.begin(9600);
  
  msg_ctrl_init();

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
    delayMicroseconds(50);
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
      for (uint8_t r = 0; r < resp->size; r++) {
        for (uint8_t c = 0; c < 7; c++) {
          if (key_matrix_is_pressed(&resp->buffer[r], c)) {
            Serial.print("Col ");
            Serial.print(c);
            Serial.print(", Row ");
            Serial.print(r);
            Serial.println(" is PRESSED");
            any_pressed = true;
          }
        }
      }
      if (!any_pressed) {
        Serial.println("No keys are pressed");
      }
    } else if (resp->kind != MSG_KIND_HEARTBEAT) {
      Serial.print("Received message of kind: 0x");
      Serial.println(resp->kind, HEX);
    }
  }

  delay(10);
}
