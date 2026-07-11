#include <iostream>
#include <cassert>
#include "tests.h"
#include "comm_mock.h"
#include <msgs.h>

TEST_START(test_msg_send_heartbeat)
    comm_mock_reset();
    msg_send_heartbeat();
    assert(mock_sent_data.size() == 1);
    assert(mock_sent_data[0] == MSG_HEARTBEAT_BYTE);
TEST_END

TEST_START(test_msg_tick_not_consumed)
    comm_mock_reset();
    mock_data_consumed_return = false;
    msg_tick();
    assert(mock_sent_data.size() == 0);
TEST_END

TEST_START(test_msg_tick_heartbeat)
    comm_mock_reset();
    msg_tick();
    assert(mock_sent_data.size() == 1);
    assert(mock_sent_data[0] == MSG_HEARTBEAT_BYTE);
TEST_END

TEST_START(test_msg_tick2)
    comm_mock_reset();
    msgs_init();

    msgs_tick2();
    assert(mock_sent_data.size() == 1);
    assert(mock_sent_data[0] == MSG_HEARTBEAT_BYTE);
TEST_END

TEST_START(test_msg_produce_keys)
    comm_mock_reset();
    msgs_init();

    msgs_msg_t msg = {};
    msg.kind = MSG_KIND_KEYS;
    msg.size = 3;
    msg.buffer[0] = 10;
    msg.buffer[1] = 20;
    msg.buffer[2] = 30;

    // Produce the message (it goes into index 1, since msgs_init leaves index 0 empty)
    msgs_produce(msg);

    // Tick 1: Processes the empty index 0, which defaults to HEARTBEAT (1 byte)
    msgs_tick2();
    assert(mock_sent_data.size() == 1);
    assert(mock_sent_data[0] == MSG_HEARTBEAT_BYTE);

    // Tick 2: Starts processing our KEYS message. Sends 'kind'
    msgs_tick2(); 
    assert(mock_sent_data.size() == 2);
    assert(mock_sent_data[1] == MSG_KIND_KEYS);

    // Tick 3: Sends 'size'
    msgs_tick2();
    assert(mock_sent_data.size() == 3);
    assert(mock_sent_data[2] == 3);

    // Tick 4: Sends buffer[0]
    msgs_tick2();
    assert(mock_sent_data.size() == 4);
    assert(mock_sent_data[3] == 10);

    // Tick 5: Sends buffer[1]
    msgs_tick2();
    assert(mock_sent_data.size() == 5);
    assert(mock_sent_data[4] == 20);

    // Tick 6: Sends buffer[2]
    msgs_tick2();
    assert(mock_sent_data.size() == 6);
    assert(mock_sent_data[5] == 30);

    // Tick 7: Message is done, should send a HEARTBEAT again!
    msgs_tick2();
    assert(mock_sent_data.size() == 7);
    assert(mock_sent_data[6] == MSG_HEARTBEAT_BYTE);
TEST_END

int main() {
    std::cout << "Running msgs tests..." << std::endl;
    
    test_msg_send_heartbeat();
    test_msg_tick_not_consumed();
    test_msg_tick_heartbeat();
    test_msg_tick2();
    test_msg_produce_keys();
    
    std::cout << "All msgs tests passed successfully!" << std::endl;
    return 0;
}
