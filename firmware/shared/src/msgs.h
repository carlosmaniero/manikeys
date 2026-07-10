#ifndef MSGS_H
#define MSGS_H

#include <stdint.h>
#include <comm.h>
#include <assert.h>

#define MSG_HEARTBEAT_BYTE 0xA5
#define MSG_MAX_MSG_SIZE 8

enum {
  MSG_KIND_HEARTBEAT = MSG_HEARTBEAT_BYTE,
  MSG_KIND_KEYS = 1
};

uint8_t msg_buffer[MSG_MAX_MSG_SIZE + 1] = {0};
uint8_t msg_buffer_len = 0;
uint8_t msg_buffer_index = 0;

void _msg_init_message(uint8_t msg_type, uint8_t *data, uint8_t data_len) {
  assert(data_len <= MSG_MAX_MSG_SIZE);

  msg_buffer_len = data_len;
  msg_buffer_index = 0;
  msg_buffer[0] = data_len;

  for (uint8_t i = 0; i < data_len; i++) {
    msg_buffer[i + 1] = data[i];
  }

  comm_send_data(msg_type);
}

void msg_send_heartbeat() {
  _msg_init_message(MSG_KIND_HEARTBEAT, 0, 0);
}

void msg_tick() {
  if (!comm_data_consumed()) {
    return;
  }

  // special case:
  // when the message has no payload (such as heartbeat_byte) we never write
  // the message size
  if (msg_buffer_len == msg_buffer_index) {
    msg_send_heartbeat();
  }

  if (msg_buffer_index < msg_buffer_len) {
    comm_send_data(msg_buffer[msg_buffer_index + 1]);
    msg_buffer_index++;
  }
}

#endif // MSGS_H
