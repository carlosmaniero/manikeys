from dataclasses import dataclass


@dataclass
class BasePlateParameters:
    screw_height: float = 1.0
    clearance: float = 0.2
    thickness: float = 2.0
