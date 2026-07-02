from dataclasses import dataclass


@dataclass
class RJ11Parameters:
    width: float
    height: float
    length: float
    bottom_notch_length: float
    bottom_notch_height: float
    bottom_notch_start_y: float
    inner_paddings: list[float]
    inner_length: float
    socket_height: float
    socket_diameter: float
    error_margin: float
    adapter_head_height: float
    adapter_socket_diameter: float
