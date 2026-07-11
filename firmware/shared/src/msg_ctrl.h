#ifndef MSG_CTRL_H
#define MSG_CTRL_H

#include <stdint.h>
#include <comm.h>
#include <msg.h>
#include <queue.h>

typedef struct {
  queue_t rx;
  queue_t tx;
} msg_ctrl_t;

extern msg_ctrl_t msg_ctrl;

void msg_ctrl_init();
void msg_ctrl_produce(msg_t msg);
void msg_ctrl_build_response();
void msg_ctrl_tick();
msg_t* msg_ctrl_consume_response();

#endif // MSG_CTRL_H
