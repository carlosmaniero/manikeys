#ifndef MSG_H
#define MSG_H

#include <stdint.h>
#include <stddef.h>

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
  bool done;
} msg_t;

inline void msg_reset(msg_t *message) {
  msg_t heartbeat_msg = {};
  heartbeat_msg.kind = MSG_KIND_HEARTBEAT;

  *message = heartbeat_msg;
}

inline bool msg_is_completed(msg_t *message) {
  uint8_t payload_offset = offsetof(msg_t, buffer);
  bool has_payload = message->kind & MSG_KIND_HAS_PAYLOAD;

  return !has_payload || message->_cursor == message->size + payload_offset;
}

#endif // MSG_H
