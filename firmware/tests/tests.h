#ifndef TESTS_H
#define TESTS_H

#include <iostream>

#define TEST_START(name) void name() { std::cout << "running: " << #name;
#define TEST_END std::cout << " - ok" << std::endl; };

#endif // TESTS_H
