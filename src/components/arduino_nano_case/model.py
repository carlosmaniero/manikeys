from dataclasses import dataclass
from injector import inject, singleton
from components.arduino_nano_case.parameters import ArduinoNanoCaseParameters
from globals.wall.parameters import WallParameters
from globals.screw.parameters import ScrewParameters


@singleton
@inject
@dataclass
class ArduinoNanoCaseModel:
    parameters: ArduinoNanoCaseParameters
    wall_parameters: WallParameters
    screw_parameters: ScrewParameters

    @property
    def wall_thickness(self) -> float:
        return self.wall_parameters.thickness

    @property
    def dimensions(self) -> list[float]:
        return [
            self.parameters.pcb_width + self.wall_thickness * 2,
            self.parameters.pcb_length + self.wall_thickness * 2,
            self.wall_thickness,
        ]

    @property
    def body_fillet_radius(self) -> float:
        return self.wall_thickness

    @property
    def tower_radius(self) -> float:
        return self.screw_hole_radius + self.wall_thickness / 2

    @property
    def tower_height(self) -> float:
        return self.parameters.screw_height

    @property
    def screw_hole_radius(self) -> float:
        return self.screw_parameters.m1_6_diameter / 2

    @property
    def tower_coords(self) -> list[list[float]]:
        x_dist = self.parameters.pcb_width / 2 - self.parameters.screw_distance
        y_dist = self.parameters.pcb_length / 2 - self.parameters.screw_distance
        z_center = self.dimensions[2] / 2 + self.tower_height / 2
        return [
            [x_dist, y_dist, z_center],
            [-x_dist, y_dist, z_center],
            [x_dist, -y_dist, z_center],
            [-x_dist, -y_dist, z_center],
        ]

    @property
    def screw_holes_height(self) -> float:
        return self.tower_height + self.dimensions[2] + 2.0

    @property
    def screw_holes_coords(self) -> list[list[float]]:
        x_dist = self.parameters.pcb_width / 2 - self.parameters.screw_distance
        y_dist = self.parameters.pcb_length / 2 - self.parameters.screw_distance
        z_center = self.tower_height / 2
        return [
            [x_dist, y_dist, z_center],
            [-x_dist, y_dist, z_center],
            [x_dist, -y_dist, z_center],
            [-x_dist, -y_dist, z_center],
        ]
