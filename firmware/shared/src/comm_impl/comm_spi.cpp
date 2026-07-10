#include "../comm.h"
#include <SPI.h>
#include <Arduino.h>

void comm_set_slave() {
  pinMode(MISO, OUTPUT);
  SPCR |= (1 << SPE);
}

void comm_respond_heartbeat() {
  SPDR = HEARTBEAT_BYTE;
}

bool comm_data_consumed() {
  return (SPSR & (1 << SPIF));
}
