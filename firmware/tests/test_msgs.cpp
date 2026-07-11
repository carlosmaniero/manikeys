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

    // Produce the message (it goes into index 1, since msgs_init leaves index 0 empty)
    msg_ctrl_produce(msg);

    // Tick 1: Processes the empty index 0, which defaults to HEARTBEAT (1 byte)
    msg_ctrl_tick();
    assert(mock_sent_data.size() == 1);
    assert(mock_sent_data[0] == MSG_HEARTBEAT_BYTE);

    // Tick 2: Starts processing our KEYS message. Sends 'kind'
    msg_ctrl_tick();
    assert(mock_sent_data.size() == 2);
    assert(mock_sent_data[1] == MSG_KIND_KEYS);

    // Tick 3: Sends 'size'
    msg_ctrl_tick();
    assert(mock_sent_data.size() == 3);
    assert(mock_sent_data[2] == 3);

    // Tick 4: Sends buffer[0]
    msg_ctrl_tick();
    assert(mock_sent_data.size() == 4);
    assert(mock_sent_data[3] == 10);

    // Tick 5: Sends buffer[1]
    msg_ctrl_tick();
    assert(mock_sent_data.size() == 5);
    assert(mock_sent_data[4] == 20);

    // Tick 6: Sends buffer[2]
    msg_ctrl_tick();
    assert(mock_sent_data.size() == 6);
    assert(mock_sent_data[5] == 30);

    // Tick 7: Message is done, should send a HEARTBEAT again!
    msg_ctrl_tick();
    assert(mock_sent_data.size() == 7);
    assert(mock_sent_data[6] == MSG_HEARTBEAT_BYTE);
TEST_END

TEST_START(test_msg_build_response)
    comm_mock_reset();
    msg_ctrl_init();

    mock_received_data_return = MSG_KIND_KEYS;
    msg_ctrl_tick();
    assert(msg_ctrl.response.done == false);
    assert(msg_ctrl.response.kind == MSG_KIND_KEYS);

    mock_received_data_return = 2;
    msg_ctrl_tick();
    assert(msg_ctrl.response.size == 2);
    assert(msg_ctrl.response.done == false);

    mock_received_data_return = 42;
    msg_ctrl_tick();
    assert(msg_ctrl.response.buffer[0] == 42);
    assert(msg_ctrl.response.done == false);

    mock_received_data_return = 99;
    msg_ctrl_tick();
    assert(msg_ctrl.response.buffer[1] == 99);

    assert(msg_ctrl.response.done == true);

    assert(msg_ctrl.response._cursor == 0);
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
    // before the overflow to happen, which is 42 (41 + 1)
    assert(mock_sent_data[2] == 42);
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
    assert(mock_sent_data[2] == MSG_HEARTBEAT_BYTE);

    msg_ctrl_tick();
    assert(mock_sent_data[3] == MSG_KIND_KEYS);
TEST_END

int main() {
    std::cout << "Running msgs tests..." << std::endl;

    test_msg_tick();
    test_msg_produce_keys();
    test_msg_build_response();
    test_msg_buffer_overflow();
    test_msg_produce_after_empty();

    std::cout << "All msgs tests passed successfully!" << std::endl;
    return 0;
}
