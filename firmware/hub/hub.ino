#include <Arduino.h>
#include <comm_spi.h>
#include <Keyboard.h>
#include <Adafruit_NeoPixel.h>
#include <msg_ctrl.h>
#include <key_matrix.h>

const uint8_t SLAVE_PIN = 9;

#define LED_PIN 10
#define NUM_LEDS 3
Adafruit_NeoPixel pixels(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

enum LedColor { LED_YELLOW, LED_GREEN, LED_RED };
static LedColor current_led_color = (LedColor)-1;

void set_led_color(LedColor color) {
  if (current_led_color == color) return;
  current_led_color = color;

  uint8_t r = 0, g = 0, b = 0;
  if (color == LED_YELLOW) {
    r = 150; g = 100; b = 0;
  } else if (color == LED_GREEN) {
    r = 0; g = 150; b = 0;
  } else if (color == LED_RED) {
    r = 150; g = 0; b = 0;
  }

  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    pixels.setPixelColor(i, pixels.Color(r, g, b));
  }
  pixels.show();
}

const char key_map[5][7] = {
  {'-', '-', '1', '2', '3', '4', '5'},
  {'-', '-', 'q', 'w', 'e', 'r', 't'},
  {'-', '-', 'a', 's', 'd', 'f', 'g'},
  {'-', '-', 'z', 'x', 'c', 'v', 'b'},
  {'-', '-', '-', '-', '-', '-', '-'}
};

const uint8_t LEFT_MATRIX_ROWS = 5;
const uint8_t LEFT_MATRIX_COLS = 5;

uint8_t left_matrix[LEFT_MATRIX_ROWS];

static unsigned long last_heard_from_slave = 0;

void setup() {
  pixels.begin();
  set_led_color(LED_YELLOW);

  Serial.begin(9600);

  msg_ctrl_init();
  key_matrix_init(left_matrix, LEFT_MATRIX_ROWS);

  Serial.println("Hub initialized. Setting up SPI...");

  comm_spi_set_master();
  comm_spi_add_slave(SLAVE_PIN);

  delay(5000);
  Keyboard.begin();
  set_led_color(LED_GREEN);
  last_heard_from_slave = millis();
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
    msg_t *rx_msg = queue_get_last(&msg_ctrl.rx);
    if (rx_msg->_cursor > 0) {
      msg_reset(rx_msg);
    }
    if (millis() - last_heard_from_slave > 2000) {
      set_led_color(LED_RED);
    }
    if (is_alive) {
      Serial.println("Error: Slave disconnected!");
      is_alive = false;
    }
  } else {
    last_heard_from_slave = millis();
    set_led_color(LED_GREEN);
    if (!is_alive) {
      Serial.println("Slave on pin 9 is ALIVE!");
      is_alive = true;
    }

    if (resp->kind == MSG_KIND_KEYS) {
      bool any_pressed = false;
      uint8_t diff[LEFT_MATRIX_ROWS];

      key_matrix_diff(left_matrix, resp->buffer, diff, LEFT_MATRIX_ROWS);

      for (uint8_t r = 0; r < resp->size; r++) {
        for (uint8_t c = 0; c < 7; c++) {
          if (key_matrix_is_active(diff + r, c)) {
            if (key_matrix_is_active(resp->buffer + r, c)) {
              key_matrix_set_pressed(left_matrix + r, c);
              char key = key_map[r][c];
              if (key != '-') {
                Keyboard.press(key);
              }
            } else {
              key_matrix_set_released(left_matrix + r, c);
              char key = key_map[r][c];
              if (key != '-') {
                Keyboard.release(key);
              }
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
