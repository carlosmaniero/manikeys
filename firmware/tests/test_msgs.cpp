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

int main() {
    std::cout << "Running msgs tests..." << std::endl;
    
    test_msg_send_heartbeat();
    test_msg_tick_not_consumed();
    test_msg_tick_heartbeat();
    
    std::cout << "All msgs tests passed successfully!" << std::endl;
    return 0;
}
