from dataclasses import dataclass
from injector import inject, singleton
from connectors.rj45_tabs.parameters import AdapterParameters
from globals.wall.parameters import WallParameters
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class AdapterModel:
    parameters: AdapterParameters
    wall_parameters: WallParameters

    @property
    def body_size(self) -> list[float]:
        return [
            self.parameters.tab_x * 2
            + self.tabs_pocket_radius * 2
            + self.wall_parameters.thickness,
            self.parameters.body_size,
            self.parameters.body_depth
        ]

    @property
    def full_body_size(self) -> list[float]:
        size = self.body_size
        size[1] += self.wall_parameters.thickness
        return size

    @property
    def mask_body_size(self) -> list[float]:
        return [
            self.full_body_size[0],
            self.full_body_size[1],
            self.wall_parameters.thickness * 10,
        ]

    @property
    def mask_shell_size(self) -> list[float]:
        return [
            self.full_body_size[0] + self.wall_parameters.thickness,
            self.full_body_size[1] + self.wall_parameters.thickness,
            self.wall_parameters.thickness * 10,
        ]

    @property
    def body_pocket(self) -> list[float]:
        return [
            self.parameters.body_size,
            self.parameters.body_size,
            self.body_size[2] - self.parameters.exposed_body_depth,
        ]

    @property
    def body_pocket_full_size(self) -> list[float]:
        return [c + self.parameters.clearance for c in self.body_pocket]

    @property
    def body_pocket_coords(self) -> list[float]:
        return [
            0,
            0,
            -self.full_body_size[2] / 2 + self.body_pocket_full_size[2] / 2,
        ]

    @property
    def exposed_body_hole_size(self) -> list[float]:
        return [
            self.parameters.exposed_body_width,
            self.parameters.exposed_body_height,
            self.parameters.exposed_body_depth,
        ]

    @property
    def exposed_body_hole_full_size(self) -> list[float]:
        with_clearance = [
            d + self.parameters.clearance for d in self.exposed_body_hole_size
        ]

        with_clearance[2] = self.full_body_size[2]
        return with_clearance

    @property
    def exposed_body_hole_coords(self) -> list[float]:
        return [
            0,
            -self.body_size[1] / 2
            + self.exposed_body_hole_full_size[1] / 2
            + self.parameters.tab_bottom_y,
            0,
        ]

    @property
    def tabs_pocket_radius(self) -> float:
        return self.parameters.tab_radius + self.parameters.clearance

    @property
    def tabs_pocket_depth(self) -> float:
        return self.body_pocket_full_size[2]

    @property
    def screw_coords(self) -> list[float]:
        return [
            self.parameters.tab_x,
            -self.body_size[1] / 2
            + self.parameters.tab_radius
            + self.parameters.tab_bottom_y,
            0,
        ]

    @property
    def tabs_pocket_coords(self) -> list[float]:
        screws = self.screw_coords
        screws[2] = -self.full_body_size[2] / 2 + self.tabs_pocket_depth / 2
        return screws

    @property
    def screw_depth(self) -> float:
        return self.full_body_size[2]

    @property
    def screw_radius(self) -> float:
        return self.parameters.screw_radius

    @property
    def screw_head_depth(self) -> float:
        return self.parameters.screw_head_depth

    @property
    def screw_head_radius(self) -> float:
        return self.parameters.screw_head_radius

    @property
    def screw_head_coords(self) -> list[float]:
        coords = self.screw_coords
        coords[2] = (
            self.full_body_size[2] / 2 - self.parameters.screw_head_depth / 2
        )
        return coords


@singleton
@inject
@dataclass
class AdapterPlacementModel:
    wall_parameters: WallParameters
    adapter_model: AdapterModel
    body_model: BodyModel

    @property
    def max_x(self) -> float:
        return self.adapter_model.full_body_size[2] / 2

    @property
    def max_y(self) -> float:
        return self.adapter_model.full_body_size[0] / 2

    @property
    def translation_coords(self) -> list[float]:
        return [
            self.body_model.end_x() - self.max_x,
            self.body_model.end_y()
            - self.wall_parameters.fillet
            - self.max_y
            - self.wall_parameters.thickness * 2,
            self.body_model.bottom_z
            + self.body_model.connectors_bottom_offset
            - self.wall_parameters.thickness / 2
            + self.adapter_model.parameters.exposed_body_height / 2,
        ]
