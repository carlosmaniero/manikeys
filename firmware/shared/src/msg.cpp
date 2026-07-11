#include <msg.h>

void msg_reset(msg_t *message) {
  msg_t heartbeat_msg = {};
  heartbeat_msg.kind = MSG_KIND_HEARTBEAT;

  *message = heartbeat_msg;
}

bool msg_is_completed(msg_t *message) {
  uint8_t payload_offset = offsetof(msg_t, buffer);
  bool has_payload = message->kind & MSG_KIND_HAS_PAYLOAD;

  return !has_payload || message->_cursor == message->size + payload_offset;
}
