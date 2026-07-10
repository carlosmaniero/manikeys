#include "../comm.h"
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
