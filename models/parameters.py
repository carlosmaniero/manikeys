from collections import namedtuple

CapsOuterParameters = namedtuple("CapsOuterParameters", ["thickness"])

CapsParameters = namedtuple(
    "CapsParameters", ["size", "thickness", "border", "outer"]
)

BodyParameters = namedtuple("BodyParameters", ["radius", "thickness"])

GlobalParameters = namedtuple("GlobalParameters", ["diff_offset"])

Parameters = namedtuple("PARAMETERS", ["caps", "body", "globals"])
