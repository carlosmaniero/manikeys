from dataclasses import dataclass


@dataclass
class CapsOuterParameters:
    thickness: float


@dataclass
class CapsParameters:
    size: float
    thickness: float
    border: float
    outer: CapsOuterParameters
    gap: float

    @property
    def full_offset(self) -> float:
        return self.size / 2 + self.border + self.gap

    @property
    def next_offset(self) -> float:
        return self.size + self.gap


@dataclass
class BodyParameters:
    radius: float
    thickness: float
    width: float
    depth: float
    height: float
    fillet: float
    cabe_hole_radius: float
    clearance: float


@dataclass
class GlobalParameters:
    diff_offset: float


@dataclass
class HandSupportParameters:
    offset_z: float
    fillet: float
    depth: float


@dataclass
class SocketAdapterParameters:
    border: float
    offset_fix: float
    diode_r: float
    diode_wire_r: float
    diode_l: float
    diode_x: float
    cube_size: float
    body_thickness: float
    cap_socket_height: float
    cap_socket_width: float


@dataclass
class Parameters:
    caps: CapsParameters
    body: BodyParameters
    globals: GlobalParameters
    hand_support: HandSupportParameters
    socket_adapter: SocketAdapterParameters
