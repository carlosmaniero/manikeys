from injector import Module, provider, singleton
from models.parameters import (
    Parameters,
    CapsParameters,
    BodyParameters,
    CapsOuterParameters,
    GlobalParameters,
    HandSupportParameters,
)


class ParametersModule(Module):
    @singleton
    @provider
    def provide_parameters(self) -> Parameters:
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
            ),
            globals=GlobalParameters(diff_offset=0.5),
            hand_support=HandSupportParameters(
                offset_z=10,
                fillet=50,
                depth=110,
            ),
        )
