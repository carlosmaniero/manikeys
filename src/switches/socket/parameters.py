from dataclasses import dataclass


@dataclass
class HotSwapParameters:
    border: float = 2.0
    offset_fix: float = 0.1
    diode_r: float = 1.4
    diode_wire_r: float = 0.75
    diode_l: float = 5.0
    diode_x: float = -4.54
    cube_size: float = 13.8
    body_thickness: float = 10.0
    switch_socket_height: float = 1.0
    switch_socket_width: float = 17.6
    center_hole_radius: float = 1.9
    mask_clearance: float = 0.2
