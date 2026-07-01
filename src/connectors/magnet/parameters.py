from dataclasses import dataclass


@dataclass
class MagnetParameters:
    diameter: float = 4.0
    height: float = 2.0
    error_margin: float = 0.15
