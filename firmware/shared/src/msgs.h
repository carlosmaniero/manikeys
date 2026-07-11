#ifndef MSGS_H
#define MSGS_H

#include <stdint.h>
#include <comm.h>
#include <assert.h>

#define MSG_HEARTBEAT_BYTE 0b01011010
#define MSG_NULL_BYTE 0b00000000
#define MSG_MAX_MSG_SIZE 8
#define MSG_MAX_MSGS 64
#define MSG_KIND_HAS_PAYLOAD 1 << 7

enum {
  MSG_KIND_HEARTBEAT = MSG_HEARTBEAT_BYTE,
  MSG_KIND_NULL = MSG_NULL_BYTE,
  MSG_KIND_KEYS = 0b10011001
};

typedef struct __attribute__((packed)) {
  uint8_t kind;
  uint8_t size;
  uint8_t buffer[MSG_MAX_MSG_SIZE];
  uint8_t _cursor;
} msgs_msg_t;

typedef struct {
  msgs_msg_t response;
  bool response_ready;
  uint8_t _cursor;
  uint8_t _latest;
  msgs_msg_t _buffer[MSG_MAX_MSGS];
} msgs_ctx_t;

msgs_ctx_t msgs_ctx;

void _msg_reset_current_message(msgs_msg_t *message) {
  msgs_msg_t heartbeat_msg = {};
  heartbeat_msg.kind = MSG_KIND_HEARTBEAT;

  *message = heartbeat_msg;
}

bool _msgs_is_message_completed(msgs_msg_t *message) {
  uint8_t payload_offset = offsetof(msgs_msg_t, buffer);
  bool has_payload = message->kind & MSG_KIND_HAS_PAYLOAD;

  return !has_payload || message->_cursor == message->size + payload_offset;
}

void msgs_init() {
  msgs_ctx = {};
  msgs_ctx._latest = 1;

  for (uint8_t i = 0; i < MSG_MAX_MSGS; i++) {
    _msg_reset_current_message(&msgs_ctx._buffer[i]);
  }
}

inline uint8_t _msgs_ctx_next_index(uint8_t cur) {
  return (cur + 1) % MSG_MAX_MSGS;
}

void msgs_produce(msgs_msg_t msg) {
  bool overflow = msgs_ctx._cursor == msgs_ctx._latest;

  if (overflow) {
    msgs_ctx._cursor = _msgs_ctx_next_index(msgs_ctx._cursor);
  }

  msgs_ctx._buffer[msgs_ctx._latest] = msg;

  msgs_ctx._latest = _msgs_ctx_next_index(msgs_ctx._latest);
}

void _msg_build_response() {
  msgs_msg_t *message = &msgs_ctx.response;

  uint8_t received = comm_received_data();

  if (message->_cursor == 0) {
    msgs_ctx.response_ready = false;
  }

  uint8_t *raw = (uint8_t*) message;

  raw[message->_cursor++] = received;

  if (_msgs_is_message_completed(message)) {
    msgs_ctx.response_ready = true;

    message->_cursor = 0; // prepare to the next message
  }
}

void msgs_tick() {
  _msg_build_response();

  msgs_msg_t *message = &msgs_ctx._buffer[msgs_ctx._cursor];

  uint8_t *raw = (uint8_t*) message;

  comm_send_data(*(raw + message->_cursor++));

  if (_msgs_is_message_completed(message)) {
    _msg_reset_current_message(message);

    msgs_ctx._cursor = _msgs_ctx_next_index(msgs_ctx._cursor);

    if (msgs_ctx._cursor == msgs_ctx._latest) {
      msgs_ctx._latest = _msgs_ctx_next_index(msgs_ctx._latest);
    }
  }
}
#endif // MSGS_H
