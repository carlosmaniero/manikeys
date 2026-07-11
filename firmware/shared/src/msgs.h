#ifndef MSGS_H
#define MSGS_H

#include <stdint.h>
#include <comm.h>
#include <assert.h>

#define MSG_HEARTBEAT_BYTE 0xA5
#define MSG_NULL_BYTE 0x00
#define MSG_MAX_MSG_SIZE 8
#define MSG_MAX_MSGS 64

enum {
  MSG_KIND_HEARTBEAT = MSG_HEARTBEAT_BYTE,
  MSG_KIND_NULL = MSG_NULL_BYTE,
  MSG_KIND_KEYS = 1
};

typedef struct __attribute__((packed)) {
  uint8_t kind;
  uint8_t size;
  uint8_t buffer[MSG_MAX_MSG_SIZE];
  uint8_t _cursor;
} msgs_msg_t;

uint8_t msg_buffer[MSG_MAX_MSG_SIZE + 1] = {};
uint8_t msg_buffer_len = 0;
uint8_t msg_buffer_index = 0;

typedef struct {
  bool ready;
  msgs_msg_t message;
  uint8_t _cursor;
  uint8_t _latest;
  msgs_msg_t _buffer[MSG_MAX_MSGS];
} msgs_ctx_t;

msgs_ctx_t msgs_ctx;

void msgs_init() {
  msgs_ctx = {};
  msgs_ctx._latest = 1;

  for (uint8_t i = 0; i < MSG_MAX_MSGS; i++) {
    msgs_ctx._buffer[i].kind = MSG_KIND_HEARTBEAT;
  }
}

inline uint8_t _msgs_ctx_next_index(uint8_t cur) {
  return (cur + 1) % (MSG_MAX_MSGS + 1);
}

void msgs_produce(msgs_msg_t msg) {
  bool overflow = msgs_ctx._cursor == msgs_ctx._latest;

  if (overflow) {
    msgs_ctx._cursor = _msgs_ctx_next_index(msgs_ctx._cursor);
  }

  msgs_ctx._buffer[msgs_ctx._latest] = msg;

  msgs_ctx._latest = _msgs_ctx_next_index(msgs_ctx._latest);
}

void _msg_reset_current_message() {
  msgs_msg_t heartbeat_msg = {};
  heartbeat_msg.kind = MSG_KIND_HEARTBEAT;

  msgs_ctx._buffer[msgs_ctx._cursor] = heartbeat_msg;
}

void msgs_tick2() {
  msgs_msg_t *message = &msgs_ctx._buffer[msgs_ctx._cursor];

  uint8_t *data = (uint8_t*) message;

  uint8_t payload_offset = offsetof(msgs_msg_t, buffer);

  comm_send_data(*(data + message->_cursor++));

  if (message->size == 0 || message->_cursor == message->size + payload_offset) {
    _msg_reset_current_message();

    if (msgs_ctx._cursor == msgs_ctx._latest) {
      msgs_ctx._latest++;
    }

    msgs_ctx._cursor++;
  }
}

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

void msg_send_keys(uint8_t* matrix, uint8_t size) {
  _msg_init_message(MSG_KIND_KEYS, matrix, size);
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
    return;
  }

  comm_send_data(msg_buffer[++msg_buffer_index]);
}

#endif // MSGS_H
