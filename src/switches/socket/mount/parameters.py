from dataclasses import dataclass


@dataclass
class MountScrewCylinderParameters:
    clearance: float = 0.2


@dataclass
class PcbsPlacementParameters:
    clearance: float = 0.2
    thickness: float = 2
    wall_margin: float = 5.0
    arduinos_offset_z: float = -15.0
