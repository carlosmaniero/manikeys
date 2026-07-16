from dataclasses import dataclass


@dataclass
class CapsOuterParameters:
    thickness: float


@dataclass
class SwitchesParameters:
    size: float
    thickness: float
    border: float
    border_shell: float
    outer: CapsOuterParameters
    gap: float

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
