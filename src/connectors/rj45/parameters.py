from dataclasses import dataclass


@dataclass
class RJ45Parameters:
    width: float = 16.0
    height: float = 13.5
    length: float = 21.0
    error_margin: float = 0.25
    socket_hole_radius: float = 1.25
    socket_hole_spacing: float = 9.0
    socket_hole_y_offset: float = 8.0
    pins_pocket_length: float = 7.0
    socket_hole_top_height: float = 0.5
    socket_hole_bottom_radius_offset: float = 1.0
