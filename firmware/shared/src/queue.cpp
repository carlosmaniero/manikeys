#include <queue.h>

uint8_t queue_next_index(uint8_t cur) {
  return (cur + 1) % MSG_MAX_MSGS;
}

void queue_append(queue_t *q, msg_t msg) {
  q->_buffer[q->_latest] = msg;
  q->_latest = queue_next_index(q->_latest);

  if (q->_cursor == q->_latest) {
    q->_cursor = queue_next_index(q->_cursor);
  }
}

msg_t* queue_get(queue_t *q) {
  if (q->_cursor == q->_latest) {
    return NULL;
  }

  return &q->_buffer[q->_cursor];
}

void queue_consume(queue_t *q) {
  msg_reset(&q->_buffer[q->_cursor]);

  q->_cursor = queue_next_index(q->_cursor);
}
