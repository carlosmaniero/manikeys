from injector import Module, provider, singleton
from models.parameters import (
    Parameters,
    CapsParameters,
    BodyParameters,
    CapsOuterParameters,
    GlobalParameters,
    HandSupportParameters,
    SocketAdapterParameters,
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
        )
