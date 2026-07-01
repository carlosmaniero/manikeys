from dataclasses import dataclass
from injector import inject, singleton
from .parameters import Parameters, RJ45Parameters
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class RJ45Model:
    parameters: Parameters

    @property
    def rj45(self) -> RJ45Parameters:
        return self.parameters.rj45

    @property
    def thickness(self) -> float:
        return self.parameters.body.thickness

    @property
    def body(self) -> list[float]:
        return [
            self.rj45.width + self.thickness * 2,
            self.rj45.length + self.thickness,
            self.rj45.height + self.thickness,
        ]

    @property
    def housing(self) -> list[float]:
        return [
            self.rj45.width + self.rj45.error_margin,
            self.rj45.length + self.rj45.error_margin / 2,
            self.rj45.height + self.rj45.error_margin / 2,
        ]

    @property
    def housing_coords(self) -> list[float]:
        return [
            0,
            self.thickness / 2,
            self.thickness / 2,
        ]

    @property
    def socket_hole_radius(self) -> float:
        return self.rj45.socket_hole_radius + self.rj45.error_margin

    @property
    def socket_hole_height(self) -> float:
        return self.thickness

    @property
    def socket_hole_top_height(self) -> float:
        return self.rj45.socket_hole_top_height

    @property
    def socket_hole_top_radius(self) -> float:
        return self.socket_hole_radius

    @property
    def socket_hole_top_coords(self) -> list[float]:
        return [
            0,
            0,
            -self.socket_hole_height / 2
            + self.socket_hole_bottom_height
            + self.socket_hole_top_height / 2,
        ]

    @property
    def socket_hole_bottom_height(self) -> float:
        return self.socket_hole_height - self.socket_hole_top_height

    @property
    def socket_hole_bottom_radius(self) -> float:
        return (
            self.socket_hole_radius + self.rj45.socket_hole_bottom_radius_offset
        )

    @property
    def socket_hole_bottom_coords(self) -> list[float]:
        return [
            0,
            0,
            -self.socket_hole_height / 2 + self.socket_hole_bottom_height / 2,
        ]

    @property
    def socket_hole_spacing(self) -> float:
        return self.rj45.socket_hole_spacing + self.socket_hole_radius

    @property
    def socket_holes_coords(self) -> list[list[float]]:
        x_offset = self.socket_hole_spacing / 2
        y_offset = (
            self.body[1] / 2
            - self.socket_hole_radius
            - self.rj45.socket_hole_y_offset
        )
        z_offset = -self.body[2] / 2 + self.socket_hole_height / 2
        return [[-x_offset, y_offset, z_offset], [x_offset, y_offset, z_offset]]

    @property
    def pins_pocket(self) -> list[float]:
        return [
            self.rj45.width,
            self.rj45.pins_pocket_length,
            self.thickness,
        ]

    @property
    def pins_pocket_coords(self) -> list[float]:
        return [
            0,
            self.pins_pocket[1] / 2 - self.body[1] / 2 + self.thickness,
            -self.body[2] / 2 + self.pins_pocket[2] / 2,
        ]

    @property
    def front_pocket(self) -> list[float]:
        return [
            self.body[0],
            self.thickness * 2 + self.rj45.error_margin,
            self.body[2],
        ]

    @property
    def front_pocket_coords(self) -> list[float]:
        return [
            0,
            self.body[1] / 2 - self.front_pocket[1] / 2,
            0,
        ]

    @property
    def front(self) -> list[float]:
        return [
            self.screw_tabs[0],
            self.front_pocket[1],
            self.front_pocket[2] + self.thickness,
        ]

    @property
    def front_coords(self) -> list[float]:
        return [
            self.front_pocket_coords[0],
            self.front_pocket_coords[1],
            self.front_pocket_coords[2] + self.thickness / 2,
        ]

    @property
    def screw_tabs(self) -> list[float]:
        return [self.body[0] + self.thickness * 4, self.thickness, self.body[2]]

    @property
    def screw_tabs_coords(self) -> list[float]:
        return [
            0,
            self.front_pocket_coords[1]
            - self.front_pocket[1] / 2
            - self.screw_tabs[1] / 2,
            0,
        ]

    @property
    def screw_hole_radius(self) -> float:
        return self.parameters.body.m2_screw_diameter / 2

    @property
    def screw_hole_height(self) -> float:
        return self.screw_tabs[1]

    @property
    def screw_hole_coords(self) -> list[list[float]]:
        x_offset = self.body[0] / 2 + self.thickness
        y_offset = self.screw_tabs_coords[1]
        z_offset = self.screw_tabs_coords[2]
        return [[-x_offset, y_offset, z_offset], [x_offset, y_offset, z_offset]]

    @property
    def front_screw_hole_coords(self) -> list[list[float]]:
        return [
            [coords[0], coords[1] - self.thickness, coords[2]]
            for coords in self.screw_hole_coords
        ]


@singleton
@inject
@dataclass
class RJ45PlacementModel:
    parameters: Parameters
    rj45_model: RJ45Model
    body_model: BodyModel

    @property
    def max_x(self) -> float:
        return self.rj45_model.screw_tabs[0] / 2

    @property
    def max_y(self) -> float:
        return self.rj45_model.body[1] / 2

    @property
    def translation_coords(self) -> list[float]:
        return [
            self.body_model.end_x() - self.parameters.body.fillet - self.max_x,
            self.body_model.end_y() - self.max_y,
            self.body_model.bottom_z + self.rj45_model.body[2] / 2,
        ]
