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
        p = self.parameters.body
        return p.m2_screw_length + p.thickness

    @property
    def z(self) -> float:
        return -self.parameters.body.height

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
