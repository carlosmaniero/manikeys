#include <msg_ctrl.h>

msg_ctrl_t msg_ctrl;

void msg_ctrl_init() {
  msg_ctrl = {};
  msg_ctrl.tx._latest = 1;

  for (uint8_t i = 0; i < MSG_MAX_MSGS; i++) {
    msg_reset(&msg_ctrl.tx._buffer[i]);
  }
}

void msg_ctrl_produce(msg_t msg) {
  queue_append(&msg_ctrl.tx, msg);
}

void msg_ctrl_build_response() {
  msg_t *message = &msg_ctrl.response;

  uint8_t received = comm_received_data();

  if (message->_cursor == 0) {
    message->done = false;
  }

  uint8_t *raw = (uint8_t*) message;

  raw[message->_cursor++] = received;

  if (msg_is_completed(message)) {
    message->done = true;

    message->_cursor = 0; // prepare to the next message
  }
}

void msg_ctrl_tick() {
  msg_ctrl_build_response();

  msg_t *message = queue_get(&msg_ctrl.tx);

  uint8_t *raw = (uint8_t*) message;

  comm_send_data(*(raw + message->_cursor++));

  if (msg_is_completed(message)) {
    queue_consume(&msg_ctrl.tx);
  }
}
