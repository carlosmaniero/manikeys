from dataclasses import dataclass


@dataclass
class BasePlateParameters:
    screw_height: float = 2.0
    clearance: float = 0.2
