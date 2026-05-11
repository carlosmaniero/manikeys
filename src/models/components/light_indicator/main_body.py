from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
from models.parameters import Parameters


@singleton
@inject
@dataclass
class MainBodyModel:
    parameters: Parameters

    @property
    def body_thickness(self) -> float:
        return self.parameters.body.thickness

    @property
    def lid_height(self) -> float:
        return self.body_thickness * 2

    @property
    def pcb_width(self) -> float:
        return 43.16

    @property
    def pcb_length(self) -> float:
        return 17.76

    @property
    def pcb_error(self) -> float:
        return 0.25

    @property
    def led_pcb_error(self) -> float:
        return 0.5

    @property
    def led_error(self) -> float:
        return 0.125

    @property
    def led_offset(self) -> float:
        pcb_mask_radius = 5 + self.led_pcb_error / 2
        pcb_mask_diameter = pcb_mask_radius * 2
        return pcb_mask_diameter + self.body_thickness / 2

    @property
    def led_x_positions(self) -> list[float]:
        return [
            -self.led_offset,
            0,
            self.led_offset,
        ]

    @property
    def pocket_depth(self) -> float:
        return self.lid_height - 1.0

    @property
    def body_depth(self) -> float:
        pocket_length = self.pcb_length + self.pcb_error * 2
        return max(15, pocket_length + self.body_thickness * 2)

    @property
    def screw_hole_radius(self) -> float:
        return self.parameters.body.m2_screw_diameter / 2

    @property
    def screw_gap(self) -> float:
        return self.body_thickness * 2

    @property
    def right_screw_xs(self) -> list[float]:
        base = self.pcb_width / 2 + self.body_thickness + self.screw_hole_radius
        return [base, base + self.screw_gap]

    @property
    def left_screw_xs(self) -> list[float]:
        base = -(
            self.pcb_width / 2
            + self.body_thickness * 5
            + self.screw_hole_radius
        )
        return [base, base - self.screw_gap]

    @property
    def left_edge(self) -> float:
        return (
            min(self.left_screw_xs)
            - self.screw_hole_radius
            - self.body_thickness
        )

    @property
    def right_edge(self) -> float:
        return (
            max(self.right_screw_xs)
            + self.screw_hole_radius
            + self.body_thickness
        )
