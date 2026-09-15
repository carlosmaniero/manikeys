from dataclasses import dataclass, field


@dataclass
class CapsOuterParameters:
    thickness: float = 1.5


@dataclass
class SwitchesParameters:
    size: float = 14.0
    thickness: float = 5.0
    border: float = 2.0
    border_shell: float = 3.0
    outer: CapsOuterParameters = field(default_factory=CapsOuterParameters)
    gap: float = 5.0
    clearance: float = 0.2
    cable_radius: float = 1.25 / 2

    cable_path_wall_thickness: float = 0.25
    col_cable_path_wall_thickness: float = 3.0
    pin_margin: float = 0.75
    pin_clearance: float = 0.05

    @property
    def full_offset(self) -> float:
        return self.size / 2 + self.border + self.gap

    @property
    def next_offset(self) -> float:
        return self.size + self.gap


@dataclass
class HandSupportParameters:
    offset_x: float
    offset_z: float
    fillet: float
    depth: float
