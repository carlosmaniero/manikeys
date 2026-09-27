from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
import math
from structure.body.models import BodyInnerModel, BodyModel
from structure.body.screws.models import ScrewPlacementModel
from globals.wall.parameters import WallParameters
from switches.model import Layout
from models.parameters import SwitchesParameters
from connectors.pogo.models import PogoPinModel
from components.female_pin_header.model import FemalePinHeaderModel
from structure.body.parameters import BodyParameters
from switches.socket.mount.parameters import (
    MountScrewCylinderParameters,
)


from switches.model import Layout
from globals.screw.parameters import ScrewParameters


@singleton
@inject
@dataclass
class MountModel(BodyInnerModel):
    layout: Layout
    screw_parameters: ScrewParameters

    @property
    def offset(self) -> float:
        # TODO: it also should have an error margin
        return super().offset - self.body_parameters.clearance

    @property
    def screw_hole_placements(
        self,
    ) -> list[tuple[float, float, float, list[float]]]:
        placements = []
        p = self.switches_parameters
        half_decorator_depth = p.size / 2 + p.border
        offset_y = half_decorator_depth + self.screw_parameters.m2_diameter

        for col_idx, col in enumerate(self.layout.grid):
            if not col:
                continue

            if col_idx % 2 == 0:
                first_key = col[0]
                key_x, key_y, _ = first_key.position
                hole_y = key_y - offset_y
                placements.append(
                    (
                        key_x,
                        hole_y,
                        float(self.z(key_x, hole_y)),
                        first_key.rotation,
                    )
                )
            else:
                last_key = col[-1]
                key_x, key_y, _ = last_key.position
                hole_y = key_y + offset_y
                placements.append(
                    (
                        key_x,
                        hole_y,
                        float(self.z(key_x, hole_y)),
                        last_key.rotation,
                    )
                )

        screw_radius = self.screw_parameters.m2_diameter / 2
        corner_margin = screw_radius + self.wall_parameters.thickness

        corner_x_min = self.main_mask_start_x + corner_margin
        corner_x_max = (
            self.main_mask_start_x + self.main_mask_width - corner_margin
        )
        corner_y_min = self.main_mask_start_y + corner_margin
        corner_y_max = (
            self.main_mask_start_y + self.main_mask_depth - corner_margin
        )

        corner_rotation = [0.0, 0.0, 0.0]
        corner_y_mid = (corner_y_min + corner_y_max) / 2

        corners = [
            (
                corner_x_min,
                corner_y_min,
                float(self.z(corner_x_min, corner_y_min)),
                corner_rotation,
            ),
            (
                corner_x_max,
                corner_y_min,
                float(self.z(corner_x_max, corner_y_min)),
                corner_rotation,
            ),
            (
                corner_x_min,
                corner_y_max,
                float(self.z(corner_x_min, corner_y_max)),
                corner_rotation,
            ),
            (
                corner_x_max,
                corner_y_max,
                float(self.z(corner_x_max, corner_y_max)),
                corner_rotation,
            ),
            (
                corner_x_max,
                corner_y_mid,
                float(self.z(corner_x_max, corner_y_mid)),
                corner_rotation,
            ),
        ]
        placements.extend(corners)

        return placements

    @property
    def main_mask_start_x(self) -> float:
        return self.start_x() + self.wall_parameters.fillet

    @property
    def main_mask_start_y(self) -> float:
        return (
            self.divider_y
            + self.wall_parameters.fillet
            - self.wall_parameters.thickness
        )

    @property
    def main_mask_width(self) -> float:
        return self.width - self.wall_parameters.fillet * 2

    @property
    def main_mask_depth(self) -> float:
        return (
            self.end_y()
            - self.wall_parameters.fillet
            - self.main_mask_start_y
            + self.wall_parameters.thickness
        )

    @property
    def main_mask_height(self) -> float:
        return (self.sphere.highest + self.body_parameters.height) * 2


@singleton
@inject
@dataclass
class MountCavityModel(MountModel):
    @property
    def offset(self) -> float:
        return super().offset - self.wall_parameters.thickness

    @property
    def start_x_fillet_end(self) -> float:
        reduction = self.body_parameters.mount_cavity_fillet_reduction
        return self.start_x() + max(
            0.0, self.wall_parameters.fillet - reduction
        )

    @property
    def end_x_fillet_end(self) -> float:
        reduction = self.body_parameters.mount_cavity_fillet_reduction
        return self.end_x() - max(0.0, self.wall_parameters.fillet - reduction)


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


@singleton
@inject
@dataclass
class MountScrewCylinderModel:
    mount_cavity_model: MountCavityModel
    screw_placement_model: ScrewPlacementModel
    wall_parameters: WallParameters
    body: BodyModel
    parameters: MountScrewCylinderParameters

    @property
    def cavity_radius(self) -> float:
        return (
            self.screw_placement_model.mask_size / 2
            + self.wall_parameters.thickness / 2
        )

    @property
    def radius(self) -> float:
        return (
            self.cavity_radius + self.screw_placement_model.screw_diameter * 4
        )

    @property
    def height(self) -> float:
        return self.wall_parameters.thickness

    @property
    def z(self) -> float:
        return (
            self.screw_placement_model.z
            + self.wall_parameters.thickness
            + self.parameters.clearance
        )

    @property
    def center_main(self) -> tuple[float, float]:
        x = (self.body.start_x() + self.body.end_x()) / 2
        y = (self.body.divider_y + self.body.end_y()) / 2
        return (x, y)

    @property
    def placements(self) -> list[tuple[float, float, float]]:
        center_main_x, center_main_y = self.center_main
        placements = []
        for x, y in self.screw_placement_model.main_points:
            center_x = x + self.screw_placement_model.standoff_size / 2
            center_y = y + self.screw_placement_model.standoff_size / 2

            if center_x < center_main_x and center_y < center_main_y:
                rotation_deg = 0.0
            elif center_x >= center_main_x and center_y < center_main_y:
                rotation_deg = 90.0
            elif center_x >= center_main_x and center_y >= center_main_y:
                rotation_deg = 180.0
            else:
                rotation_deg = 270.0

            placements.append((center_x, center_y, rotation_deg))
        return placements

    @property
    def hole_radius(self) -> float:
        return self.screw_placement_model.screw_diameter / 2

    @property
    def hole_distance(self) -> float:
        return (self.cavity_radius + self.radius) / 2

    @property
    def hole_placements(self) -> list[tuple[float, float]]:
        center_main_x, center_main_y = self.center_main
        holes = []
        for center_x, center_y, rotation_deg in self.placements:
            dx = center_main_x - center_x
            dy = center_main_y - center_y
            target_angle = math.degrees(math.atan2(dy, dx))
            rad = math.radians(target_angle)

            hx = center_x + self.hole_distance * math.cos(rad)
            hy = center_y + self.hole_distance * math.sin(rad)
            holes.append((hx, hy))
        return holes
