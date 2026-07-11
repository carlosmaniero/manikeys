#ifndef QUEUE_H
#define QUEUE_H

#include <msg.h>

typedef struct {
  uint8_t _cursor;
  uint8_t _latest;
  msg_t _buffer[MSG_MAX_MSGS];
} queue_t;

uint8_t queue_next_index(uint8_t cur);
void queue_append(queue_t *q, msg_t msg);
msg_t* queue_get(queue_t *q);
void queue_consume(queue_t *q);

#endif // QUEUE_H
