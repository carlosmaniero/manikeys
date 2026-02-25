from injector import Module, provider, singleton
from models.parameters import (
    Parameters,
    CapsParameters,
    BodyParameters,
    CapsOuterParameters,
    GlobalParameters,
)


class ParametersModule(Module):
    @singleton
    @provider
    def provide_parameters(self) -> Parameters:
        return Parameters(
            caps=CapsParameters(
                size=14,
                thickness=5,
                border=0.5,
                gap=2.5,
                outer=CapsOuterParameters(thickness=1.5),
            ),
            body=BodyParameters(radius=300, thickness=5, width=150, depth=130),
            globals=GlobalParameters(diff_offset=0.5),
        )
