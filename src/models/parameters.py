from collections import namedtuple

CapsOuterParameters = namedtuple("CapsOuterParameters", ["thickness"])

CapsParameters = namedtuple(
    "CapsParameters", ["size", "thickness", "border", "outer", "gap"]
)

BodyParameters = namedtuple(
    "BodyParameters", ["radius", "thickness", "width", "depth"]
)

GlobalParameters = namedtuple("GlobalParameters", ["diff_offset"])

Parameters = namedtuple("PARAMETERS", ["caps", "body", "globals"])
