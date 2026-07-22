from dataclasses import dataclass


@dataclass
class FemalePinHeaderParameters:
    pitch: float = 2.54
    header_width: float = 2.54
    header_height: float = 7.0
    clearance: float = 0.2
    wall_thickness: float = 1.2
