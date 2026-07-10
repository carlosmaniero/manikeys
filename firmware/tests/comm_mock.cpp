#include "comm_mock.h"
#include <comm.h>

std::vector<uint8_t> mock_sent_data;
bool mock_data_consumed_return = true;

void comm_mock_reset() {
    mock_sent_data.clear();
    mock_data_consumed_return = true;
}

void comm_set_slave() {}

void comm_send_data(uint8_t data) {
    mock_sent_data.push_back(data);
}

bool comm_data_consumed() {
    return mock_data_consumed_return;
}
