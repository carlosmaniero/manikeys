#ifndef COMM_H
#define COMM_H

#define HEARTBEAT_BYTE 0xA5

void comm_set_slave();
void comm_respond_heartbeat();
bool comm_data_consumed();

#endif // COMM_H
