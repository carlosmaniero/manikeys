from dataclasses import dataclass


@dataclass
class USBCParameters:
    width: float
    height: float
    length: float
    pcb_thickness: float
    hole_spacing: float
    aperture: float
    num_holes: int
    error_margin: float
