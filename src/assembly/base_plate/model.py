from dataclasses import dataclass
from injector import inject, singleton
from structure.body.screws.models import ScrewPlacementModel
from structure.body.parameters import BodyParameters
from globals.wall.parameters import WallParameters
from assembly.base_plate.parameters import BasePlateParameters


@singleton
@inject
@dataclass
class BasePlateModel:
    screw_placement_model: ScrewPlacementModel
    body_parameters: BodyParameters
    wall_parameters: WallParameters
    parameters: BasePlateParameters

    @property
    def dimensions(self) -> list[float]:
        return [
            self.screw_placement_model.body.width
            - self.wall_parameters.thickness * 2
            - self.parameters.clearance * 2,
            self.screw_placement_model.body.depth
            - self.wall_parameters.thickness * 2
            - self.parameters.clearance * 2,
            self.parameters.thickness,
        ]

    @property
    def coords(self) -> list[float]:
        return [
            self.screw_placement_model.body.start_x()
            + self.wall_parameters.thickness
            + self.parameters.clearance,
            self.screw_placement_model.body.start_y()
            + self.wall_parameters.thickness
            + self.parameters.clearance,
            -(
                self.body_parameters.height
                + self.screw_placement_model.bottom_thickness
                + self.parameters.z_offset
            ),
        ]

    @property
    def screw_head_radius(self) -> float:
        return self.screw_placement_model.screw_head_diameter / 2

    @property
    def screw_head_height(self) -> float:
        return self.parameters.thickness - self.parameters.screw_height

    @property
    def screw_head_coords(self) -> list[list[float]]:
        coords = []
        z = self.coords[2]
        for x, y in self.screw_placement_model.get_centered_points():
            coords.append([x, y, z])
        return coords

    @property
    def screw_hole_radius(self) -> float:
        return self.screw_placement_model.screw_diameter / 2

    @property
    def screw_hole_height(self) -> float:
        return self.parameters.screw_height

    @property
    def screw_hole_coords(self) -> list[list[float]]:
        coords = []
        z = self.coords[2] + self.screw_head_height
        for x, y in self.screw_placement_model.get_centered_points():
            coords.append([x, y, z])
        return coords

    @property
    def mask_dimensions(self) -> list[float]:
        return [
            self.screw_placement_model.body.width
            - self.wall_parameters.thickness * 2,
            self.screw_placement_model.body.depth
            - self.wall_parameters.thickness * 2,
            self.parameters.thickness,
        ]

    @property
    def mask_coords(self) -> list[float]:
        return [
            self.screw_placement_model.body.start_x()
            + self.wall_parameters.thickness,
            self.screw_placement_model.body.start_y()
            + self.wall_parameters.thickness,
            self.screw_placement_model.bottom_z,
        ]

    @property
    def divider_dimensions(self) -> list[float]:
        divider_size = self.wall_parameters.thickness * 2
        return [
            self.screw_placement_model.body.width,
            divider_size,
            self.dimensions[2],
        ]

    @property
    def divider_coords(self) -> list[float]:
        divider_size = self.divider_dimensions[1]
        divider_y = self.screw_placement_model.body.divider_y - divider_size / 2
        return [
            self.screw_placement_model.body.start_x(),
            divider_y,
            self.coords[2],
        ]

    @property
    def mask_divider_dimensions(self) -> list[float]:
        divider_size = (
            self.wall_parameters.thickness * 2 - self.parameters.clearance
        )
        return [
            self.screw_placement_model.body.width,
            divider_size,
            self.mask_dimensions[2],
        ]

    @property
    def mask_divider_coords(self) -> list[float]:
        divider_size = self.mask_divider_dimensions[1]
        divider_y = self.screw_placement_model.body.divider_y - divider_size / 2
        return [
            self.screw_placement_model.body.start_x(),
            divider_y,
            self.mask_coords[2],
        ]
