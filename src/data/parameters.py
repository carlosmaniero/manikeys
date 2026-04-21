from injector import Module, provider, singleton
from models.parameters import (
    Parameters,
    CapsParameters,
    BodyParameters,
    CapsOuterParameters,
    GlobalParameters,
    HandSupportParameters,
    SocketAdapterParameters,
    RJ11Parameters,
    USBCParameters,
)


class ParametersModule(Module):
    @singleton
    @provider
    def provide_parameters(self) -> Parameters:
        cube_size = 13.6
        return Parameters(
            caps=CapsParameters(
                size=14,
                thickness=5,
                border=2,
                gap=5,
                outer=CapsOuterParameters(thickness=1.5),
            ),
            body=BodyParameters(
                radius=280,
                thickness=3,
                width=180,
                depth=130,
                height=15,
                fillet=10,
                cabe_hole_radius=10,
                clearance=2,
                m2_screw_diameter=2.0,
                m2_screw_length=8.0,
                m2_screw_head_diameter=4.0,
                m2_screw_head_height=2.0,
                bottom_thickness=10.0,
            ),
            globals=GlobalParameters(diff_offset=0.5),
            hand_support=HandSupportParameters(
                offset_x=75,
                offset_z=10,
                fillet=40,
                depth=110,
            ),
            socket_adapter=SocketAdapterParameters(
                border=2,
                offset_fix=0.1,
                diode_r=1.4,
                diode_wire_r=0.5,
                diode_l=5,
                diode_x=-2.54 - 2,
                cube_size=cube_size,
                body_thickness=6,
                cap_socket_height=2,
                cap_socket_width=cube_size + 4,
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
        )
