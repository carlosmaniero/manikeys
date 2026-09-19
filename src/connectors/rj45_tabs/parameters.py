from dataclasses import dataclass


@dataclass
class AdapterParameters:
    body_size: float = 22.0
    full_width: float = 26.0
    body_depth: float = 7.0
    screw_center: float = 14.0
    tab_bottom_y: float = 5.6
    tab_x: float = 14.0
    tab_radius: float = 5
    exposed_body_width: float = 16
    exposed_body_height: float = 13
    exposed_body_depth: float = 1
    clearance: float = 0.2
