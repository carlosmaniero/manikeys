#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

const uint8_t KEY_PINS[] = {3, 4, 5, 6};
const uint8_t NUM_KEYS = 4;
const char* KEY_NAMES[] = {"D3", "D4", "D5", "D6"};

bool lastState[NUM_KEYS];

void displayMessage(const char* line1, const char* line2) {
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 10);
  display.println(line1);
  if (line2 != NULL) {
    display.setCursor(0, 35);
    display.println(line2);
  }
  display.display();
}

void setup() {
  for (uint8_t i = 0; i < NUM_KEYS; i++) {
    pinMode(KEY_PINS[i], INPUT_PULLUP);
    lastState[i] = digitalRead(KEY_PINS[i]);
  }

  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    for (;;);
  }

  displayMessage("Hello", "World");
}

void loop() {
  for (uint8_t i = 0; i < NUM_KEYS; i++) {
    bool currentState = digitalRead(KEY_PINS[i]);
    if (lastState[i] == HIGH && currentState == LOW) {
      displayMessage("Pressed:", KEY_NAMES[i]);
    }
    lastState[i] = currentState;
  }
  delay(10);
}
