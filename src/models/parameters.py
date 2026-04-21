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
    m2_screw_diameter: float
    m2_screw_length: float
    m2_screw_head_diameter: float
    m2_screw_head_height: float
    bottom_thickness: float


@dataclass
class GlobalParameters:
    diff_offset: float


@dataclass
class HandSupportParameters:
    offset_x: float
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
class RJ11Parameters:
    width: float
    height: float
    length: float
    bottom_notch_length: float
    bottom_notch_height: float
    bottom_notch_start_y: float
    inner_paddings: list[float]
    inner_length: float
    socket_height: float
    socket_diameter: float
    error_margin: float
    adapter_head_height: float
    adapter_socket_diameter: float


@dataclass
class USBCParameters:
    width: float
    height: float
    length: float
    pcb_thickness: float
    hole_spacing: float
    aperture: float
    num_holes: int
    error_margin: float


@dataclass
class Parameters:
    caps: CapsParameters
    body: BodyParameters
    globals: GlobalParameters
    hand_support: HandSupportParameters
    socket_adapter: SocketAdapterParameters
    rj11: RJ11Parameters
    usbc: USBCParameters
