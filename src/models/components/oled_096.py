from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
from models.parameters import Oled096Parameters, Parameters
from models.cap_thumb import CapThumbModel
from structure.body.models import BodyModel
import math


@singleton
@inject
@dataclass
class Oled096Model:
    global_parameters: Parameters

    @property
    def parameters(self) -> Oled096Parameters:
        return self.global_parameters.oled096

    @property
    def thickness(self) -> float:
        return self.global_parameters.body.thickness

    @property
    def pcb_pocket(self) -> list[float]:
        return [
            self.pcb_with_clearance[0],
            self.pcb_with_clearance[1],
            self.body[2] - self.parameters.display_height,
        ]

    @property
    def pcb_with_clearance(self) -> list[float]:
        return [d + self.parameters.clearance for d in self.parameters.pcb]

    @property
    def panel_pocket(self) -> list[float]:
        return [
            self.parameters.panel[0] + self.parameters.clearance,
            self.parameters.panel[1] + self.parameters.clearance,
            self.parameters.panel[2] + self.parameters.clearance,
        ]

    @property
    def pcb_pocket_coords(self) -> list[float]:
        return [0.0, 0.0, -self.parameters.display_height / 2]

    @property
    def panel_pocket_coords(self) -> list[float]:
        return [0.0, 0.0, self.body[2] / 2 - self.parameters.panel[2] / 2]

    @property
    def body(self) -> list[float]:
        return [
            self.pcb_with_clearance[0] + self.thickness * 4,
            self.pcb_with_clearance[1] + self.thickness * 4,
            self.pcb_with_clearance[2]
            + self.parameters.display_height
            + self.thickness,
        ]

    @property
    def screw_holes(self) -> list[list[float]]:
        first_col_x = self.parameters.screw_hole_offset
        second_col_x = self.body[0] - self.parameters.screw_hole_offset

        z = (
            self.parameters.screw_hole_depth / 2
            - self.body[2] / 2
            + self.thickness
        )
        z = math.floor(z * 100) / 100

        return [
            [first_col_x, 0, z],
            [second_col_x, 0, z],
        ]

    @property
    def screw_holes_translation(self) -> list[float]:
        return [
            -self.body[0] / 2,
            0,
            0.0,
        ]

    @property
    def cable_clearance(self) -> list[float]:
        return [
            self.parameters.cable_clearance[0],
            self.parameters.cable_clearance[1],
            self.pcb_pocket[2],
        ]

    @property
    def cable_clearance_coords(self) -> list[float]:
        return [
            0.0,
            self.pcb_pocket[1] / 2 + self.parameters.cable_clearance[1] / 2,
            -self.body[2] / 2 + self.pcb_pocket[2] / 2,
        ]

    @property
    def lid_pocket(self) -> list[float]:
        return [
            self.body[0],
            self.parameters.panel[1] + self.parameters.clearance,
            self.thickness,
        ]

    @property
    def lid_pocket_coords(self) -> list[float]:
        return [
            0.0,
            0.0,
            -self.body[2] / 2 + self.thickness / 2,
        ]


@singleton
@inject
@dataclass
class Oled096PlacementModel:
    global_parameters: Parameters
    oled: Oled096Model
    cap_thumb: CapThumbModel

    @property
    def thickness(self) -> float:
        return self.global_parameters.body.thickness

    @property
    def body_model(self) -> BodyModel:
        return self.cap_thumb.body_model

    @property
    def placement_position(self) -> list[float]:
        x = (
            self.body_model.hand_support_end_x
            + self.global_parameters.caps.full_offset
            + self.thickness * 3
        )
        y = (
            self.body_model.divider_y
            - self.global_parameters.caps.full_offset
            - self.thickness
        )
        z = self.body_model.sphere.highest - self.oled.body[2] / 2
        return [x, y, z]

    @property
    def mask_size(self) -> list[float]:
        height_z = self.body_model.highest - self.body_model.bottom_z
        return [
            self.oled.body[0],
            self.oled.body[1] - self.thickness * 2,
            height_z,
        ]

    @property
    def mask_coords(self) -> list[float]:
        height_z = self.body_model.highest - self.body_model.bottom_z
        x = self.placement_position[0]
        y = self.placement_position[1] - self.thickness
        z = self.body_model.highest - height_z / 2
        return [x, y, z]

    @property
    def shell_mask_size(self) -> list[float]:
        return [
            self.oled.body[0] + self.thickness,
            self.oled.body[1] + self.thickness,
            self.oled.body[2] + self.thickness,
        ]

    @property
    def shell_mask_coords(self) -> list[float]:
        return self.placement_position
