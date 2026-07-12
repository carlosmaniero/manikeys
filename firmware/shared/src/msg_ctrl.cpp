#include <msg_ctrl.h>

msg_ctrl_t msg_ctrl;

void msg_ctrl_init() {
  msg_ctrl = {};
}

void msg_ctrl_produce(msg_t msg) {
  queue_append(&msg_ctrl.tx, msg);
}

void msg_ctrl_build_response() {
  msg_t *message = queue_get_last(&msg_ctrl.rx);

  uint8_t received = comm_received_data();

  if (message->_cursor == 0) {
    message->done = false;
  }

  uint8_t *raw = (uint8_t*) message;

  raw[message->_cursor++] = received;

  if (msg_is_completed(message)) {
    message->done = true;

    message->_cursor = 0;

    queue_commit_last(&msg_ctrl.rx);
  }
}

void msg_ctrl_tick() {
  msg_ctrl_build_response();

  msg_t *message = queue_get(&msg_ctrl.tx);

  if (message == NULL) {
    comm_send_data(MSG_HEARTBEAT_BYTE);
    return;
  }

  uint8_t *raw = (uint8_t*) message;

  comm_send_data(*(raw + message->_cursor++));

  if (msg_is_completed(message)) {
    queue_consume(&msg_ctrl.tx);
  }
}

void msg_ctrl_tick_all() {
  msg_ctrl_tick();

  while (true) {
    msg_t *rx_msg = queue_get_last(&msg_ctrl.rx);
    msg_t *tx_msg = queue_get(&msg_ctrl.tx);

    bool rx_in_progress = (rx_msg != NULL && rx_msg->_cursor > 0);
    bool tx_in_progress = (tx_msg != NULL && tx_msg->_cursor > 0);

    if (!rx_in_progress && !tx_in_progress) {
      break;
    }

    while (!comm_data_consumed()) {
      if (comm_is_deselected()) {
        return;
      }
    }

    msg_ctrl_tick();
  }
}

msg_t* msg_ctrl_consume_response() {
  msg_t *message = queue_get(&msg_ctrl.rx);
  if (message == NULL) {
    return NULL;
  }

  static msg_t response_copy;
  response_copy = *message;
  queue_consume(&msg_ctrl.rx);
  return &response_copy;
}
