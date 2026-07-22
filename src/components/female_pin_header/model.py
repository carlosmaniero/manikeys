from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
from components.female_pin_header.parameters import FemalePinHeaderParameters


@singleton
@inject
@dataclass
class FemalePinHeaderModel:
    parameters: FemalePinHeaderParameters

    def inner_length(self, pins: int) -> float:
        return (pins * self.parameters.pitch) + self.parameters.clearance

    @property
    def inner_width(self) -> float:
        return self.parameters.header_width + self.parameters.clearance

    @property
    def inner_height(self) -> float:
        return self.parameters.header_height + self.parameters.clearance

    def outer_length(self, pins: int) -> float:
        return self.inner_length(pins) + (self.parameters.wall_thickness * 2)

    @property
    def outer_width(self) -> float:
        return self.inner_width + (self.parameters.wall_thickness * 2)

    @property
    def outer_height(self) -> float:
        return self.inner_height + self.parameters.wall_thickness

    def wire_hole_length(self, pins: int) -> float:
        return self.inner_length(pins) - 1.0

    @property
    def wire_hole_width(self) -> float:
        return self.inner_width - 1.0
