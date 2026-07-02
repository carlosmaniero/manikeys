from globals.screw.parameters import ScrewParameters
from globals.wall.parameters import WallParameters
from dataclasses import dataclass
from switches.socket.parameters import HotSwapParameters
from structure.body.parameters import BodyParameters
from connectors.pogo.parameters import PogoPinParameters
from connectors.magnet.parameters import MagnetParameters
from components.oled_096.parameters import Oled096Parameters
from connectors.rj45.parameters import RJ45Parameters


@dataclass
class CapsOuterParameters:
    thickness: float


@dataclass
class SwitchesParameters:
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
    screw: ScrewParameters
    wall: WallParameters
    switches: SwitchesParameters
    body: BodyParameters
    hand_support: HandSupportParameters
    hot_swap: HotSwapParameters
    rj11: RJ11Parameters
    rj45: RJ45Parameters
    usbc: USBCParameters
    pogo_pin: PogoPinParameters
    magnet: MagnetParameters
    oled096: Oled096Parameters
