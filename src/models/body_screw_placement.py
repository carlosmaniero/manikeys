from dataclasses import dataclass
from injector import inject, singleton
from .body import BodyModel
from .parameters import Parameters


@singleton
@inject
@dataclass
class BodyScrewPlacementModel:
    body: BodyModel
    parameters: Parameters

    @property
    def cube_size(self) -> float:
        p = self.parameters.body
        return p.m2_screw_diameter + p.thickness * 2

    @property
    def cube_height(self) -> float:
        return self.mask_height

    @property
    def mask_size(self) -> float:
        return self.cube_size + self.parameters.body.thickness

    @property
    def mask_height(self) -> float:
        return 1000

    @property
    def z(self) -> float:
        return -self.parameters.body.height

    @property
    def mask_z(self) -> float:
        return -500

    @property
    def main_points(self) -> list[tuple[float, float]]:
        x_start = self.body.start_x()
        x_end = self.body.end_x() - self.cube_size
        y_divider = self.body.divider_y
        y_end = self.body.end_y() - self.cube_size

        return [
            (x_start, y_divider),
            (x_end, y_divider),
            (x_start, y_end),
            (x_end, y_end),
        ]

    @property
    def hand_points(self) -> list[tuple[float, float]]:
        x_start = self.body.hand_support_end_x
        x_end = self.body.end_x() - self.cube_size
        y_start = self.body.start_y()
        y_divider_end = self.body.divider_y - self.cube_size

        return [
            (x_start, y_start),
            (x_end, y_start),
            (x_start, y_divider_end),
            (x_end, y_divider_end),
        ]

    @property
    def points(self) -> list[tuple[float, float]]:
        return self.main_points + self.hand_points

    @property
    def screw_diameter(self) -> float:
        return self.parameters.body.m2_screw_diameter

    @property
    def screw_height(self) -> float:
        return self.parameters.body.m2_screw_length

    @property
    def screw_z(self) -> float:
        return self.z

    def get_centered_points(self) -> list[tuple[float, float]]:
        offset = self.cube_size / 2
        return [(x + offset, y + offset) for x, y in self.points]

    def get_mask_points(self) -> list[tuple[float, float]]:
        offset = (self.mask_size - self.cube_size) / 2
        return [(x - offset, y - offset) for x, y in self.points]
