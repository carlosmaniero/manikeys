from dataclasses import dataclass


@dataclass
class MountScrewCylinderParameters:
    clearance: float = 0.2
    extra_radius: float = 6.0


@dataclass
class PcbsPlacementParameters:
    clearance: float = 0.2
    thickness: float = 2
    wall_margin: float = 5.0
    arduinos_offset_z: float = -15.0


@dataclass
class MountScrewHoleParameters:
    offset_z: float = -0.1
    height: float = 4.0


@dataclass
class PcbShellMainParameters:
    cutout_extra_size: float = 3.0
    thickness: float = 3.0


@dataclass
class PcbShellMainGuideParameters:
    thickness: float = 2.0
