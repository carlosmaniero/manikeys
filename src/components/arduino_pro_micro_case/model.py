from dataclasses import dataclass
from injector import inject, singleton
from components.arduino_pro_micro_case.parameters import (
    ArduinoProMicroCaseParameters,
)
from globals.wall.parameters import WallParameters
from globals.screw.parameters import ScrewParameters


@singleton
@inject
@dataclass
class ArduinoProMicroCaseModel:
    parameters: ArduinoProMicroCaseParameters
    wall_parameters: WallParameters
    screw_parameters: ScrewParameters

    @property
    def wall_thickness(self) -> float:
        return self.wall_parameters.thickness

    @property
    def dimensions(self) -> list[float]:
        original_depth = self.parameters.depth + self.parameters.clearance
        return [
            self.pcb_placement_dimensions[0] + self.wall_thickness * 4,
            self.usb_c_cutout_dimensions[1]
            + self.parameters.usb_c_offset
            + self.parameters.clearance,
            original_depth + self.wall_thickness,
        ]

    @property
    def pcb_placement_dimensions(self) -> list[float]:
        return [
            self.parameters.width + self.parameters.clearance,
            self.parameters.height + self.parameters.clearance,
            (self.parameters.depth + self.parameters.clearance) * 2,
        ]

    @property
    def pcb_placement_coords(self) -> list[float]:
        return [
            0,
            0,
            self.dimensions[2] / 2,
        ]

    @property
    def usb_c_cylinder_radius(self) -> float:
        return self.usb_c_cutout_dimensions[2] / 2

    @property
    def usb_c_cylinder_height(self) -> float:
        return self.usb_c_cutout_dimensions[1]

    @property
    def usb_c_cylinder_offset(self) -> float:
        return self.usb_c_cutout_dimensions[0] / 2 - self.usb_c_cylinder_radius

    @property
    def screw_hole_radius(self) -> float:
        return self.screw_parameters.m2_diameter / 2

    @property
    def screw_head_radius(self) -> float:
        return self.screw_parameters.m2_head_diameter / 2

    @property
    def screw_head_height(self) -> float:
        return (
            self.lid_dimensions[2] - self.parameters.expected_screw_hole_height
        )

    @property
    def screw_holes_coords(self) -> list[list[float]]:
        x_offset = self.dimensions[0] / 2 - self.wall_thickness
        return [
            [-x_offset, 0, 0],
            [x_offset, 0, 0],
        ]

    @property
    def usb_c_cutout_dimensions(self) -> list[float]:
        dimensions = [
            self.parameters.usb_c_width,
            self.parameters.usb_c_offset + self.pcb_placement_dimensions[1],
            self.parameters.usb_c_radius * 2,
        ]

        return [
            dimension + self.parameters.clearance for dimension in dimensions
        ]

    @property
    def usb_c_cutout_coords(self) -> list[float]:
        return [
            0,
            -(self.parameters.usb_c_offset + self.parameters.clearance) / 2,
            self.dimensions[2] / 2 + self.usb_c_cutout_dimensions[2] / 2,
        ]

    @property
    def lid_thickness(self) -> float:
        return self.wall_thickness * 2

    @property
    def lid_dimensions(self) -> list[float]:
        return [
            self.dimensions[0],
            self.dimensions[1],
            self.lid_thickness,
        ]

    @property
    def lid_coords(self) -> list[float]:
        return [
            0,
            0,
            self.dimensions[2] / 2 + self.lid_thickness / 2,
        ]

    @property
    def pins_clearance_dimensions(self) -> list[float]:
        return [
            self.parameters.pins_clearance,
            self.parameters.height,
            self.dimensions[2],
        ]

    @property
    def pins_clearance_coords(self) -> list[list[float]]:
        x_offset = (
            self.parameters.width / 2 - self.parameters.pins_clearance / 2
        )
        return [
            [-x_offset, 0, 0],
            [x_offset, 0, 0],
        ]

    @property
    def pins_clearance_radius(self) -> float:
        return self.pins_clearance_dimensions[0] / 2

    @property
    def pins_clearance_y_offset(self) -> float:
        return (
            self.pins_clearance_dimensions[1] / 2 - self.pins_clearance_radius
        )

    @property
    def body_fillet_radius(self) -> float:
        return self.wall_thickness
