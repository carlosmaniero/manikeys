from dataclasses import dataclass


@dataclass
class ArduinoProMicroCaseParameters:
    width: float = 18.5
    height: float = 35.0
    depth: float = 1.1

    clearance: float = 0.5

    usb_c_radius: float = 1.5
    usb_c_offset: float = 2.0
    usb_c_width: float = 9

    pins_clearance: float = 3.5
    expected_screw_hole_height: float = 1.5
