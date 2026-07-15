#include <iostream>
#include <cassert>
#include "tests.h"
#include "comm_mock.h"
#include <msg_ctrl.h>


TEST_START(test_msg_tick)
    comm_mock_reset();
    msg_ctrl_init();

    msg_ctrl_tick();
    assert(mock_sent_data.size() == 1);
    assert(mock_sent_data[0] == MSG_HEARTBEAT_BYTE);
TEST_END

TEST_START(test_msg_produce_keys)
    comm_mock_reset();
    msg_ctrl_init();

    msg_t msg = {};
    msg.kind = MSG_KIND_KEYS;
    msg.size = 3;
    msg.buffer[0] = 10;
    msg.buffer[1] = 20;
    msg.buffer[2] = 30;

    msg_ctrl_produce(msg);

    msg_ctrl_tick();
    assert(mock_sent_data[0] == MSG_KIND_KEYS);

    msg_ctrl_tick();
    assert(mock_sent_data.size() == 2);

    msg_ctrl_tick();
    assert(mock_sent_data.size() == 3);
    assert(mock_sent_data[1] == 3);

    msg_ctrl_tick();
    assert(mock_sent_data.size() == 4);
    assert(mock_sent_data[2] == 10);

    msg_ctrl_tick();
    assert(mock_sent_data.size() == 5);
    assert(mock_sent_data[3] == 20);

    msg_ctrl_tick();
    assert(mock_sent_data.size() == 6);
    assert(mock_sent_data[4] == 30);

    msg_ctrl_tick();
    assert(mock_sent_data.size() == 7);
    assert(mock_sent_data[5] == MSG_HEARTBEAT_BYTE);
TEST_END

TEST_START(test_msg_build_response)
    comm_mock_reset();
    msg_ctrl_init();

    mock_received_data_return = MSG_KIND_KEYS;
    msg_ctrl_tick();
    assert(queue_get_last(&msg_ctrl.rx)->done == false);
    assert(queue_get_last(&msg_ctrl.rx)->kind == MSG_KIND_KEYS);

    mock_received_data_return = 2;
    msg_ctrl_tick();
    assert(queue_get_last(&msg_ctrl.rx)->size == 2);
    assert(queue_get_last(&msg_ctrl.rx)->done == false);

    mock_received_data_return = 42;
    msg_ctrl_tick();
    assert(queue_get_last(&msg_ctrl.rx)->buffer[0] == 42);
    assert(queue_get_last(&msg_ctrl.rx)->done == false);

    mock_received_data_return = 99;
    msg_ctrl_tick();

    msg_t *completed = msg_ctrl_consume_response();
    assert(completed != NULL);
    assert(completed->buffer[1] == 99);
    assert(completed->done == true);
    assert(completed->_cursor == 0);
TEST_END

TEST_START(test_msg_queue_multiple_responses)
    comm_mock_reset();
    msg_ctrl_init();

    mock_received_data_return = MSG_KIND_HEARTBEAT;
    msg_ctrl_tick();
    msg_t *msg1 = msg_ctrl_consume_response();
    assert(msg1 != NULL);
    assert(msg1->kind == MSG_KIND_HEARTBEAT);

    mock_received_data_return = MSG_KIND_HEARTBEAT;
    msg_ctrl_tick();
    msg_t *msg2 = msg_ctrl_consume_response();
    assert(msg2 != NULL);
    assert(msg2->kind == MSG_KIND_HEARTBEAT);
TEST_END

TEST_START(test_msg_buffer_overflow)
    comm_mock_reset();
    msg_ctrl_init();

    for (uint8_t i = 0; i < MSG_MAX_MSGS + 1; i++) {
        msg_t msg = {};
        msg.kind = MSG_KIND_KEYS;
        msg.size = 1;
        msg.buffer[0] = 41 + i;
        msg_ctrl_produce(msg);
    }

    msg_ctrl_tick();
    assert(mock_sent_data[0] == MSG_KIND_KEYS);

    msg_ctrl_tick();
    assert(mock_sent_data[1] == 1);

    msg_ctrl_tick();
    // Once the buffer was overflowed, the next message the first message
    // before the overflow to happen, which is 43 (41 + 2)
    assert(mock_sent_data[2] == 43);
TEST_END

TEST_START(test_msg_produce_after_empty)
    comm_mock_reset();
    msg_ctrl_init();

    msg_ctrl_tick();
    msg_ctrl_tick();

    msg_t msg = {};
    msg.kind = MSG_KIND_KEYS;
    msg.size = 1;
    msg.buffer[0] = 99;
    msg_ctrl_produce(msg);

    msg_ctrl_tick();
    assert(mock_sent_data[2] == MSG_KIND_KEYS);
TEST_END

TEST_START(test_msg_tick_all)
    comm_mock_reset();
    msg_ctrl_init();

    // Verify msg_ctrl_tick_all compiles and runs
    msg_ctrl_tick_all();
    assert(mock_sent_data.size() == 1);
    assert(mock_sent_data[0] == MSG_HEARTBEAT_BYTE);
TEST_END

int main() {
    std::cout << "Running slave msgs tests..." << std::endl;

    test_msg_tick();
    test_msg_produce_keys();
    test_msg_build_response();
    test_msg_queue_multiple_responses();
    test_msg_buffer_overflow();
    test_msg_produce_after_empty();
    test_msg_tick_all();

    std::cout << "All slave msgs tests passed successfully!" << std::endl;
    return 0;
}
