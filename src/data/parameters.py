from globals.screw.parameters import ScrewParameters
from globals.wall.parameters import WallParameters
from injector import Module, provider, singleton
from models.parameters import (
    SwitchesParameters,
    CapsOuterParameters,
    HandSupportParameters,
)
from switches.socket.parameters import HotSwapParameters
from structure.body.parameters import BodyParameters
from connectors.pogo.parameters import PogoPinParameters
from connectors.magnet.parameters import MagnetParameters
from connectors.rj45.parameters import RJ45Parameters
from connectors.usbc.parameters import USBCParameters
from components.oled_096.parameters import Oled096Parameters
from connectors.rj11.parameters import RJ11Parameters


class ParametersModule(Module):
    @singleton
    @provider
    def provide_switches_parameters(self) -> SwitchesParameters:
        return SwitchesParameters(
            size=14,
            thickness=5,
            border=2,
            gap=5,
            outer=CapsOuterParameters(thickness=1.5),
        )

    @singleton
    @provider
    def provide_body_parameters(self) -> BodyParameters:
        return BodyParameters()

    @singleton
    @provider
    def provide_wall_parameters(self) -> WallParameters:
        return WallParameters()

    @singleton
    @provider
    def provide_hot_swap_parameters(self) -> HotSwapParameters:
        return HotSwapParameters()

    @singleton
    @provider
    def provide_screw_parameters(self) -> ScrewParameters:
        return ScrewParameters()

    @singleton
    @provider
    def provide_hand_support_parameters(self) -> HandSupportParameters:
        return HandSupportParameters(
            offset_x=75,
            offset_z=10,
            fillet=40,
            depth=110,
        )

    @singleton
    @provider
    def provide_rj11_parameters(self) -> RJ11Parameters:
        return RJ11Parameters(
            width=11.0,
            height=11.5,
            length=18.2,
            bottom_notch_length=6.0,
            bottom_notch_height=0.5,
            bottom_notch_start_y=5.0,
            inner_paddings=[2.0, 1.5, 3.0, 1.5],
            inner_length=12.0,
            socket_height=4.4,
            socket_diameter=2.0,
            error_margin=0.25,
            adapter_head_height=2.5,
            adapter_socket_diameter=3.0,
        )

    @singleton
    @provider
    def provide_rj45_parameters(self) -> RJ45Parameters:
        return RJ45Parameters()

    @singleton
    @provider
    def provide_usbc_parameters(self) -> USBCParameters:
        return USBCParameters(
            width=13.0,
            height=4.8,
            length=22.0,
            pcb_thickness=1.6,
            hole_spacing=2.54,
            aperture=1.0,
            num_holes=6,
            error_margin=0.25,
        )

    @singleton
    @provider
    def provide_pogo_pin_parameters(self) -> PogoPinParameters:
        return PogoPinParameters()

    @singleton
    @provider
    def provide_magnet_parameters(self) -> MagnetParameters:
        return MagnetParameters()

    @singleton
    @provider
    def provide_oled096_parameters(self) -> Oled096Parameters:
        return Oled096Parameters()
