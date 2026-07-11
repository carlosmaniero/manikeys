#include "comm_mock.h"
#include <comm.h>

std::vector<uint8_t> mock_sent_data;
bool mock_data_consumed_return = true;
uint8_t mock_received_data_return = 0;

void comm_mock_reset() {
    mock_sent_data.clear();
    mock_data_consumed_return = true;
    mock_received_data_return = 0;
}

void comm_set_slave() {}

void comm_send_data(uint8_t data) {
    mock_sent_data.push_back(data);
}

bool comm_data_consumed() {
    return mock_data_consumed_return;
}

uint8_t comm_received_data() {
    return mock_received_data_return;
}
