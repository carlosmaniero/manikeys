#include <comm.h>
#include <msgs.h>

void setup() {
  comm_set_slave();
  msg_send_heartbeat();
}

void loop() {
  msg_tick();
}
