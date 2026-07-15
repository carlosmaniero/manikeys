#ifndef COMM_H
#define COMM_H
#include<stdint.h>

void comm_set_slave();
void comm_send_heartbeat();
void comm_send_data(uint8_t data);
bool comm_data_consumed();
uint8_t comm_received_data();
bool comm_is_deselected();

#endif // COMM_H
