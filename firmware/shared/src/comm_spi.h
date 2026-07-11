#ifndef COMM_SPI_H
#define COMM_SPI_H

#include <stdint.h>

void comm_spi_set_master();
void comm_spi_add_slave(uint8_t ss_pin);
void comm_spi_start_transaction(uint8_t ss_pin);
uint8_t comm_spi_transfer(uint8_t data);
void comm_spi_end_transaction(uint8_t ss_pin);

#endif // COMM_SPI_H
