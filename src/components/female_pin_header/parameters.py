from dataclasses import dataclass


@dataclass
class FemalePinHeaderParameters:
    pitch: float = 2.54
    header_width: float = 2.54
    header_height: float = 7.0
    clearance: float = 0.20
    wall_thickness: float = 1.2
    wire_diameter: float = 1.2
    angle: float = 45.0
    ledge_gap: float = 1.0
