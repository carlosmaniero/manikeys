from globals.screw.parameters import ScrewParameters
from globals.wall.parameters import WallParameters
from dataclasses import dataclass
from structure.body.parameters import BodyParameters


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
    center_hole_radius: float


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
class RJ45Parameters:
    @property
    def width(self) -> float:
        return 16.0

    @property
    def height(self) -> float:
        return 13.5

    @property
    def length(self) -> float:
        return 21.0

    @property
    def error_margin(self) -> float:
        return 0.25

    @property
    def socket_hole_radius(self) -> float:
        return 1.25

    @property
    def socket_hole_spacing(self) -> float:
        return 9

    @property
    def socket_hole_y_offset(self) -> float:
        return 8

    @property
    def pins_pocket_length(self) -> float:
        return 7.0

    @property
    def socket_hole_top_height(self) -> float:
        return 0.5

    @property
    def socket_hole_bottom_radius_offset(self) -> float:
        return 1.0


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
class PogoPinParameters:
    body_length: float
    body_width: float
    body_height: float
    flange_thickness: float
    mounting_hole_diameter: float
    mounting_hole_distance: float
    pin_pitch: float
    pin_count: int
    magnet_distance: float
    pin_height: float
    pin_tip_diameter: float
    solder_tail_diameter: float
    solder_tail_length: float


@dataclass
class MagnetParameters:
    diameter: float
    height: float
    error_margin: float


@dataclass
class Oled096Parameters:
    @property
    def display_height(self) -> float:
        return 1.5

    @property
    def pcb(self) -> list[float]:
        return [24.7, 27, 1.5]

    @property
    def panel(self) -> list[float]:
        return [24.74, 16.9, self.display_height]

    @property
    def clearance(self) -> float:
        return 0.5

    @property
    def screw_hole_offset(self) -> float:
        return 2

    @property
    def flat_cable_clearance(self) -> float:
        return 0.25

    @property
    def flat_cable_width(self) -> float:
        return 9.0

    @property
    def cable_clearance(self) -> list[float]:
        return [10.0, 2.0]


@dataclass
class Parameters:
    screw: ScrewParameters
    wall: WallParameters
    caps: CapsParameters
    body: BodyParameters
    hand_support: HandSupportParameters
    socket_adapter: SocketAdapterParameters
    rj11: RJ11Parameters
    rj45: RJ45Parameters
    usbc: USBCParameters
    pogo_pin: PogoPinParameters
    magnet: MagnetParameters
    oled096: Oled096Parameters
