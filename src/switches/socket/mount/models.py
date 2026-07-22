from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
from structure.body.models import BodyInnerModel
from globals.wall.parameters import WallParameters
from switches.model import Layout
from models.parameters import SwitchesParameters


@singleton
@inject
@dataclass
class MountModel(BodyInnerModel):
    @property
    def offset(self) -> float:
        # TODO: it also should have an error margin
        return super().offset - self.body_parameters.clearance


@singleton
@inject
@dataclass
class MountCavityModel(MountModel):
    @property
    def offset(self) -> float:
        return super().offset - self.wall_parameters.thickness


@singleton
@inject
@dataclass
class ColCablePathModel:
    body_model: MountCavityModel
    wall_parameters: WallParameters
    layout: Layout
    switches_parameters: SwitchesParameters

    @property
    def cable_radius(self) -> float:
        return self.switches_parameters.cable_radius

    @property
    def outer_radius(self) -> float:
        return self.cable_radius + 0.8

    @property
    def path(self) -> list[tuple[float, float, float, float]]:
        base_thickness = self.wall_parameters.thickness * 2
        offset_x = self.wall_parameters.thickness
        last_key = len(self.layout.grid) - 1
        cols = len(self.layout.grid[last_key])

        paths = []
        max_height = 0
        z = self.body_model.highest - base_thickness * 3

        for col in range(cols):
            first_key = self.layout.grid[last_key][col]
            x = self.body_model.end_x() - offset_x
            y = first_key.position[1]

            if col == 0:
                height = self.wall_parameters.thickness
            else:
                height = self.wall_parameters.thickness * (col + 2) / 2

            max_height = max(max_height, height)
            z_min = z - height
            paths.append((x, y, z_min, height))

        z_min_bigger = z - max_height
        first_key = self.layout.grid[last_key][0]
        y_first = first_key.position[1]
        z_min_new = z_min_bigger - self.wall_parameters.thickness * 3
        height_new = self.wall_parameters.thickness

        for col in range(cols):
            x = self.body_model.end_x() - offset_x
            y = y_first + col * (self.outer_radius + self.cable_radius)
            paths.append((x, y, z_min_new, height_new))

        return paths
