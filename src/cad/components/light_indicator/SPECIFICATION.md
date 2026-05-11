# Light Indicator Specification

The light indicator component is designed to work with an Arduino Nano and WS2812B chips.

## Components

- **Controller**: Arduino Nano
- **LEDs**: [WS2812B Chips](https://pt.aliexpress.com/item/4000879938744.html?spm=a2g0o.order_list.order_list_main.187.b014caa4U7BhXU&gatewayAdapt=glo2bra)

## Wiring Diagram

The indicator soldering pins should be connected as follows:

| Indicator Pin | Arduino Nano Pin | Notes |
| :--- | :--- | :--- |
| **VCC** | 5V | |
| **GND** | Ground | |
| **DIN** | D6 | Data In |
| **SDA** | A4 | I2C Data |
| **SCL** | A5 | I2C Clock |
