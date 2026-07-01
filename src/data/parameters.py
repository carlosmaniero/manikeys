from globals.screw.parameters import ScrewParameters
from globals.wall.parameters import WallParameters
from injector import Module, provider, singleton
from models.parameters import (
    Parameters,
    SwitchesParameters,
    CapsOuterParameters,
    HandSupportParameters,
    HotSwapParameters,
    RJ11Parameters,
    RJ45Parameters,
    USBCParameters,
    PogoPinParameters,
    MagnetParameters,
    Oled096Parameters,
)
from structure.body.parameters import BodyParameters


class ParametersModule(Module):
    @singleton
    @provider
    def provide_parameters(self) -> Parameters:
        return Parameters(
            switches=SwitchesParameters(
                size=14,
                thickness=5,
                border=2,
                gap=5,
                outer=CapsOuterParameters(thickness=1.5),
            ),
            body=BodyParameters(),
            wall=WallParameters(),
            hot_swap=HotSwapParameters(),
            screw=ScrewParameters(),
            hand_support=HandSupportParameters(
                offset_x=75,
                offset_z=10,
                fillet=40,
                depth=110,
            ),
            rj11=RJ11Parameters(
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
            ),
            rj45=RJ45Parameters(),
            usbc=USBCParameters(
                width=13.0,
                height=4.8,
                length=22.0,
                pcb_thickness=1.6,
                hole_spacing=2.54,
                aperture=1.0,
                num_holes=6,
                error_margin=0.25,
            ),
            pogo_pin=PogoPinParameters(
                body_length=31.00,
                body_width=4.50,
                body_height=4.00,
                flange_thickness=1.00,
                mounting_hole_diameter=1.50,
                mounting_hole_distance=34.50,
                pin_pitch=2.54,
                pin_count=9,
                magnet_distance=27.00,
                pin_height=5.00,
                pin_tip_diameter=0.90,
                solder_tail_diameter=0.70,
                solder_tail_length=1.50,
            ),
            magnet=MagnetParameters(
                diameter=4.0,
                height=2.0,
                error_margin=0.15,
            ),
            oled096=Oled096Parameters(),
        )
