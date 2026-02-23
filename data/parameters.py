from models.parameters import (
    Parameters,
    CapsParameters,
    BodyParameters,
    CapsOuterParameters,
    GlobalParameters,
)

parameters = Parameters(
    caps=CapsParameters(
        size=14, thickness=5, border=2, outer=CapsOuterParameters(thickness=1.5)
    ),
    body=BodyParameters(radius=300, thickness=3),
    globals=GlobalParameters(diff_offset=0.5),
)
