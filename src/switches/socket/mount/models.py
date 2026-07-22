from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
from structure.body.models import BodyInnerModel
from globals.wall.parameters import WallParameters
from switches.model import Layout
from models.parameters import SwitchesParameters
from connectors.pogo.models import PogoPinModel


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


from components.female_pin_header.model import FemalePinHeaderModel


@singleton
@inject
@dataclass
class ColCablePathModel:
    body_model: MountCavityModel
    wall_parameters: WallParameters
    layout: Layout
    switches_parameters: SwitchesParameters
    female_pin_header_model: FemalePinHeaderModel

    @property
    def cable_radius(self) -> float:
        return self.switches_parameters.cable_radius

    @property
    def outer_radius(self) -> float:
        return self.cable_radius + 0.8

    @property
    def pin_header_position(self) -> tuple[float, float, float]:
        y_center = (self.body_model.end_y() + self.body_model.divider_y) / 2

        z_pos = (
            self.body_model.bottom_z
            + self.female_pin_header_model.inner_height
            + self.wall_parameters.thickness
        )
        x = (
            self.body_model.end_x()
            - self.wall_parameters.thickness
            - self.female_pin_header_model.outer_width / 2
        )
        return (x, y_center, z_pos)

    @property
    def path(self) -> list[tuple[float, float, float, float]]:
        base_thickness = self.wall_parameters.thickness * 2
        offset_x = self.wall_parameters.thickness
        last_key = len(self.layout.grid) - 1
        cols = len(self.layout.grid[last_key])

        paths = []
        z = self.body_model.highest - base_thickness * 3

        for col in range(cols):
            first_key = self.layout.grid[last_key][col]
            x = (
                self.body_model.end_x()
                - offset_x
                - (self.outer_radius + self.cable_radius)
            )
            y = first_key.position[1]

            height = self.wall_parameters.thickness

            z_min = z - height
            paths.append((x, y, z_min, height))

        return paths


from structure.body.parameters import BodyParameters


@singleton
@inject
@dataclass
class RowCablePathModel:
    body_model: MountCavityModel
    wall_parameters: WallParameters
    body_parameters: BodyParameters
    layout: Layout
    female_pin_header_model: FemalePinHeaderModel
    pogo_model: PogoPinModel

    @property
    def pin_header_position(self) -> tuple[float, float, float]:
        pogo_radius = self.pogo_model.adapter_width / 2
        x_pogo = (
            self.body_model.end_x()
            - pogo_radius
            - self.wall_parameters.thickness * 3
        )
        x = (
            x_pogo
            - pogo_radius
            - self.wall_parameters.thickness
            - self.female_pin_header_model.outer_length(len(self.layout.grid))
            / 2
        )
        divider_size = (
            self.wall_parameters.thickness * 2
            + self.body_parameters.clearance * 2
        )
        y = (
            self.body_model.divider_y
            + divider_size / 2
            + self.female_pin_header_model.outer_width / 2
            + self.wall_parameters.thickness * 2
        )
        z_pos = (
            self.body_model.bottom_z
            + self.female_pin_header_model.inner_height
            + self.wall_parameters.thickness
        )
        return (x, y, z_pos)

    @property
    def path(self) -> list[tuple[float, float, float, float]]:
        return []
