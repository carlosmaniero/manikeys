from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
from models.parameters import Oled096Parameters, Parameters
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
