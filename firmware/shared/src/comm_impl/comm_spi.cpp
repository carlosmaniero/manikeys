#include "../comm.h"
#include "../comm_spi.h"
#include <SPI.h>
#include <Arduino.h>

#if defined(IS_MASTER)

// ==========================================
// MASTER IMPLEMENTATION
// ==========================================

void comm_set_slave() {}

bool comm_data_consumed() {
  return true;
}

uint8_t last_received_data = 0;

void comm_prepare_message(uint8_t data) {
  last_received_data = SPI.transfer(data);
}

void comm_send_data() {}

uint8_t comm_received_data() {
  return last_received_data;
}

bool comm_is_deselected() {
  return false;
}

void comm_spi_set_master() {
  SPI.begin();
}

void comm_spi_add_slave(uint8_t ss_pin) {
  pinMode(ss_pin, OUTPUT);
  digitalWrite(ss_pin, HIGH);
}

void comm_spi_start_transaction(uint8_t ss_pin) {
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  digitalWrite(ss_pin, LOW);
}

uint8_t comm_spi_transfer(uint8_t data) {
  last_received_data = SPI.transfer(data);
  return last_received_data;
}

void comm_spi_end_transaction(uint8_t ss_pin) {
  digitalWrite(ss_pin, HIGH);
  SPI.endTransaction();
}

#else

// ==========================================
// SLAVE IMPLEMENTATION
// ==========================================

void comm_set_slave() {
  pinMode(MISO, OUTPUT);
  SPCR |= (1 << SPE) | (1 << SPIE);
}

uint8_t message_to_be_sent = 0;

bool comm_data_consumed() {
  return (SPSR & (1 << SPIF));
}

void comm_prepare_message(uint8_t data) {
  message_to_be_sent = data;
}

void comm_send_data() {
  SPDR = message_to_be_sent;
}

uint8_t comm_received_data() {
  return SPDR;
}

bool comm_is_deselected() {
#ifdef ARDUINO
#if defined(__AVR_ATmega328P__)
  return (PINB & (1 << PB2));
#else
  return (digitalRead(SS) == HIGH);
#endif
#else
  return false;
#endif
}

#endif
