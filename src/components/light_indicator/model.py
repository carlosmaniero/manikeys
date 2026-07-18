from __future__ import annotations
from globals.wall.parameters import WallParameters
from globals.screw.parameters import ScrewParameters
from dataclasses import dataclass
from injector import inject, singleton
from components.light_indicator.parameters import LedParameters
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class LightIndicatorModel:
    wall_parameters: WallParameters
    screw_parameters: ScrewParameters
    led: LedParameters
    body_model: BodyModel

    @property
    def body_thickness(self) -> float:
        return self.wall_parameters.thickness * 4

    @property
    def transparent_panel_thickness(self) -> float:
        return 1.0

    @property
    def external_panel_radius(self) -> float:
        return 0.5

    @property
    def margin_thickness(self) -> float:
        return self.wall_parameters.thickness

    @property
    def lid_height(self) -> float:
        return self.margin_thickness * 2

    @property
    def leds_section(self) -> float:
        return (
            max(self.led_x_positions)
            - min(self.led_x_positions)
            - self.led_pcb_radius
        )

    @property
    def pcb_length(self) -> float:
        return 17.76

    @property
    def pcb_error(self) -> float:
        return 0.25

    @property
    def panel_error(self) -> float:
        return 0.25

    @property
    def led_pcb_error(self) -> float:
        return 0.5

    @property
    def led_error(self) -> float:
        return 0.125

    @property
    def led_pcb_radius(self) -> float:
        return self.led.pcb_radius + self.led_pcb_error / 2

    @property
    def led_offset(self) -> float:
        pcb_mask_radius = self.led_pcb_radius
        pcb_mask_diameter = pcb_mask_radius * 2
        return pcb_mask_diameter + self.margin_thickness / 2

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
        return self.led.pcb_radius * 2 + self.margin_thickness

    @property
    def screw_hole_radius(self) -> float:
        return self.screw_parameters.m2_diameter / 2

    @property
    def right_screw_x(self) -> float:
        return self.leds_section + self.margin_thickness

    @property
    def left_screw_x(self) -> float:
        return -(self.right_screw_x)

    @property
    def width(self) -> float:
        return (
            self.right_screw_x + self.screw_hole_radius + self.margin_thickness
        ) * 2

    @property
    def placement_rotation(self) -> list[float]:
        return [0, 0, 90]

    @property
    def placement_translation(self) -> list[float]:
        r = self.body_depth / 2
        height = self.margin_thickness * 2

        t1_x = (-self.width / 2) / 2 - r * 2

        return [
            self.body_model.start_fixed_x + 12,
            t1_x
            + self.body_model.end_y()
            - self.wall_parameters.fillet
            - self.wall_parameters.thickness,
            self.body_model.highest - height / 2,
        ]
