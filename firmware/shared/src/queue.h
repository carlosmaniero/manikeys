#ifndef QUEUE_H
#define QUEUE_H

#include <msg.h>

typedef struct {
  uint8_t _cursor;
  uint8_t _latest;
  msg_t _buffer[MSG_MAX_MSGS];
} queue_t;

inline uint8_t queue_next_index(uint8_t cur) {
  return (cur + 1) % MSG_MAX_MSGS;
}

inline void queue_append(queue_t *q, msg_t msg) {
  bool overflow = q->_cursor == q->_latest;

  if (overflow) {
    q->_cursor = queue_next_index(q->_cursor);
  }

  q->_buffer[q->_latest] = msg;
  q->_latest = queue_next_index(q->_latest);
}

inline msg_t* queue_get(queue_t *q) {
  return &q->_buffer[q->_cursor];
}

inline void queue_consume(queue_t *q) {
  msg_reset(&q->_buffer[q->_cursor]);

  if (queue_next_index(q->_cursor) == q->_latest) {
    q->_latest = queue_next_index(q->_latest);
  }

  q->_cursor = queue_next_index(q->_cursor);
}

#endif // QUEUE_H
