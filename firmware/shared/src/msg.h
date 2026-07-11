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

void msg_reset(msg_t *message);
bool msg_is_completed(msg_t *message);

#endif // MSG_H
