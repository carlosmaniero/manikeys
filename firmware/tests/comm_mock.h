#ifndef COMM_MOCK_H
#define COMM_MOCK_H

#include <stdint.h>
#include <vector>

extern std::vector<uint8_t> mock_sent_data;
extern bool mock_data_consumed_return;

void comm_mock_reset();

#endif
