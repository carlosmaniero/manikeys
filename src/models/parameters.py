from globals.screw.parameters import ScrewParameters
from globals.wall.parameters import WallParameters
from dataclasses import dataclass
from switches.socket.parameters import HotSwapParameters
from structure.body.parameters import BodyParameters
from connectors.pogo.parameters import PogoPinParameters
from connectors.magnet.parameters import MagnetParameters
from components.oled_096.parameters import Oled096Parameters
from connectors.rj45.parameters import RJ45Parameters
from connectors.usbc.parameters import USBCParameters
from connectors.rj11.parameters import RJ11Parameters


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
