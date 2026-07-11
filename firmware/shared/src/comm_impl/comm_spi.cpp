#include "../comm.h"
#include "../comm_spi.h"
#include <SPI.h>
#include <Arduino.h>

void comm_set_slave() {
  pinMode(MISO, OUTPUT);
  SPCR |= (1 << SPE);
}


bool comm_data_consumed() {
  return (SPSR & (1 << SPIF));
}

void comm_send_data(uint8_t data) {
  SPDR = data;
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
  return SPI.transfer(data);
}

void comm_spi_end_transaction(uint8_t ss_pin) {
  digitalWrite(ss_pin, HIGH);
  SPI.endTransaction();
}
