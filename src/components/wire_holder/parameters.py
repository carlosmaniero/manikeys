from dataclasses import dataclass


@dataclass
class WireHolderParameters:
    pitch: float = 2.0
    clearance: float = 0.2
    wall_thickness: float = 1.2
    width: float = 3.0
    height: float = 3.0
    hole_diameter: float = 2.0
