from dataclasses import dataclass


@dataclass
class CapsOuterParameters:
    thickness: float


@dataclass
class CapsParameters:
    size: float
    thickness: float
    border: float
    outer: CapsOuterParameters
    gap: float


@dataclass
class BodyParameters:
    radius: float
    thickness: float
    width: float
    depth: float


@dataclass
class GlobalParameters:
    diff_offset: float


@dataclass
class Parameters:
    caps: CapsParameters
    body: BodyParameters
    globals: GlobalParameters
