from dataclasses import dataclass


@dataclass
class CableHookParameters:
    cable_radius: float = 0.5
    wall_thickness: float = 0.8
    height: float = 1.0
