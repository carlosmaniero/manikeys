#include "../comm.h"
#include "../comm_spi.h"
#include <SPI.h>
#include <Arduino.h>

void comm_set_slave() {
  pinMode(MISO, OUTPUT);
  SPCR |= (1 << SPE) | (1 << SPIE);
}

bool is_master = false;
uint8_t last_received_data = 0;


bool comm_data_consumed() {
  if (is_master) {
    return true;
  }

  return (SPSR & (1 << SPIF));
}

void comm_send_data(uint8_t data) {
  if (is_master) {
    last_received_data = SPI.transfer(data);
    return;
  }
  SPDR = data;
}

uint8_t comm_received_data() {
  if (is_master) {
    return last_received_data;
  }

  return SPDR;
}

void comm_spi_set_master() {
  is_master = true;
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
