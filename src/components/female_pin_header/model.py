from __future__ import annotations
import math
from dataclasses import dataclass
from injector import inject, singleton
from components.female_pin_header.parameters import FemalePinHeaderParameters


@singleton
@inject
@dataclass
class FemalePinHeaderModel:
    parameters: FemalePinHeaderParameters

    @property
    def top_left_y(self) -> float:
        return self.parameters.header_height / math.cos(
            math.radians(self.parameters.angle)
        )

    @property
    def top_left_x(self) -> float:
        return self.parameters.header_height / math.sin(
            math.radians(self.parameters.angle)
        )

    @property
    def pocket_width(self) -> float:
        return self.parameters.header_width + self.parameters.clearance

    @property
    def top_right_y(self) -> float:
        return self.top_left_y - self.pocket_width * math.cos(
            math.radians(self.parameters.angle)
        )

    @property
    def top_right_x(self) -> float:
        return self.top_left_x + self.pocket_width * math.sin(
            math.radians(self.parameters.angle)
        )

    @property
    def bottom_right_x(self) -> float:
        return (
            self.pocket_width
            / math.cos(math.radians(self.parameters.angle))
            / math.tan(math.radians(self.parameters.angle))
        )

    @property
    def front_x(self) -> float:
        return -(self.parameters.wire_diameter + self.parameters.wall_thickness)

    @property
    def full_body_points(self) -> list[tuple[float, float]]:
        return [
            (self.front_x, 0),
            (self.front_x, self.top_left_y),
            (self.top_left_x, self.top_left_y),
            (self.top_right_x, self.top_right_y),
            (self.top_right_x, 0),
        ]

    @property
    def pocket_body_points(self) -> list[tuple[float, float]]:
        height = self.parameters.header_height - self.parameters.wall_thickness

        top_left_x = height / math.sin(math.radians(self.parameters.angle))
        top_left_y = height / math.cos(math.radians(self.parameters.angle))

        top_right_y = top_left_y - self.pocket_width * math.cos(
            math.radians(self.parameters.angle)
        )
        top_right_x = top_left_x + self.pocket_width * math.sin(
            math.radians(self.parameters.angle)
        )

        return [
            (0, 0),
            (top_left_x, top_left_y),
            (top_right_x, top_right_y),
            (self.bottom_right_x, 0),
        ]

    @property
    def pocket_pins_points(self) -> list[tuple[float, float]]:
        return [
            (0, 0),
            (self.top_left_x, self.top_left_y),
            (self.top_right_x, self.top_right_y),
            (self.bottom_right_x, 0),
        ]

    def pocket_length(self, pins: int):
        return self.parameters.header_width * pins + self.parameters.clearance

    def pin_length(self, pins: int):
        return self.pocket_length(pins) - self.parameters.ledge_gap

    def outer_length(self, pins: int):
        return self.pocket_length(pins) + self.parameters.wall_thickness * 2

    @property
    def wire_path_x(self) -> float:
        d = self.parameters.wire_diameter
        return self.front_x + self.parameters.wall_thickness + d / 2

    @property
    def wire_path_y(self) -> float:
        return self.top_left_y / 2
