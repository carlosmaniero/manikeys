from globals.wall.parameters import WallParameters
from globals.screw.parameters import ScrewParameters
from structure.body.parameters import BodyParameters
from dataclasses import dataclass
from injector import inject, singleton
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class ScrewPlacementModel:
    body: BodyModel
    wall_parameters: WallParameters
    screw_parameters: ScrewParameters
    body_parameters: BodyParameters

    @property
    def standoff_size(self) -> float:
        return (
            self.screw_parameters.m2_diameter + self.wall_parameters.thickness
        )

    @property
    def standoff_height(self) -> float:
        return self.body.highest - self.z

    @property
    def mask_size(self) -> float:
        return self.standoff_size * 2 + self.wall_parameters.thickness

    @property
    def mask_height(self) -> float:
        return self.body.height

    @property
    def z(self) -> float:
        return self.bottom_z + self.bottom_thickness

    @property
    def mask_z(self) -> float:
        return self.bottom_z

    @property
    def main_points(self) -> list[tuple[float, float]]:
        x_start = self.body.start_x() + self.wall_parameters.thickness
        x_end = (
            self.body.end_x()
            - self.standoff_size
            - self.wall_parameters.thickness
        )
        y_divider = self.body.divider_y + self.wall_parameters.thickness
        y_end = (
            self.body.end_y()
            - self.standoff_size
            - self.wall_parameters.thickness
        )

        return [
            (x_start, y_divider),
            (x_end, y_divider),
            (x_start, y_end),
            (x_end, y_end),
        ]

    @property
    def hand_points(self) -> list[tuple[float, float]]:
        x_start = self.body.hand_support_end_x + self.wall_parameters.thickness
        x_end = (
            self.body.end_x()
            - self.standoff_size
            - self.wall_parameters.thickness
        )
        y_start = self.body.start_y() + self.wall_parameters.thickness
        y_divider_end = (
            self.body.divider_y
            - self.standoff_size
            - self.wall_parameters.thickness
        )

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
    def screw_head_diameter(self) -> float:
        return self.screw_parameters.m2_head_diameter

    @property
    def screw_head_height(self) -> float:
        return self.screw_parameters.m2_head_height

    @property
    def bottom_thickness(self) -> float:
        return self.body_parameters.bottom_thickness

    @property
    def bottom_z(self) -> float:
        return self.body.bottom_z

    @property
    def screw_head_z(self) -> float:
        return self.bottom_z

    @property
    def screw_diameter(self) -> float:
        return self.screw_parameters.m2_diameter

    @property
    def screw_height(self) -> float:
        return self.screw_parameters.m2_length

    @property
    def screw_z(self) -> float:
        return self.z

    def get_centered_points(self) -> list[tuple[float, float]]:
        offset = self.standoff_size / 2
        return [(x + offset, y + offset) for x, y in self.points]

    def get_mask_points(self) -> list[tuple[float, float]]:
        offset = (self.mask_size - self.standoff_size) / 2
        return [(x - offset, y - offset) for x, y in self.points]
