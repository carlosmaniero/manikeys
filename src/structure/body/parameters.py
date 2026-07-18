from dataclasses import dataclass


@dataclass
class BodyParameters:
    radius: float = 280.0
    width: float = 180.0
    depth: float = 130.0
    height: float = 25.0
    cabe_hole_radius: float = 13.0
    clearance: float = 2.0
    bottom_thickness: float = 5.0
    connectors_bottom_offset: float = 10.0

    @property
    def bottom_z(self) -> float:
        return -self.height - self.bottom_thickness
