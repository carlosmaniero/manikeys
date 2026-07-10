#include <comm.h>

void setup() {
  comm_set_slave();
  comm_respond_heartbeat();
}

void loop() {
  if (comm_data_consumed()) {
    comm_respond_heartbeat();
  }
}
