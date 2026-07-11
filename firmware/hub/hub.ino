#include <Arduino.h>
#include <comm_spi.h>
#include <msg_ctrl.h>

const uint8_t SLAVE_PIN = 9;

void setup() {
  Serial.begin(9600);
  
  while (!Serial) {
    ; 
  }
  
  Serial.println("Hub initialized. Setting up SPI...");
  
  comm_spi_set_master();
  comm_spi_add_slave(SLAVE_PIN);
}

void loop() {
  comm_spi_start_transaction(SLAVE_PIN);
  
  uint8_t response = comm_spi_transfer(MSG_NULL_BYTE);
  
  comm_spi_end_transaction(SLAVE_PIN);
  
  if (response == MSG_HEARTBEAT_BYTE) {
    Serial.println("Slave on pin 9 is ALIVE! (Received Heartbeat)");
  } else {
    Serial.print("Slave is dead or not ready. Received: 0x");
    Serial.println(response, HEX);
  }
  
  delay(10);
}
