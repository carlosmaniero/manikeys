from dataclasses import dataclass
from injector import inject, singleton
from structure.body.screws.models import ScrewPlacementModel
from structure.body.parameters import BodyParameters
from globals.wall.parameters import WallParameters
from assembly.base_plate.parameters import BasePlateParameters
from components.arduino_nano_case.model import ArduinoNanoCaseModel
from components.arduino_pro_micro_case.model import ArduinoProMicroCaseModel


@singleton
@inject
@dataclass
class BasePlateModel:
    screw_placement_model: ScrewPlacementModel
    body_parameters: BodyParameters
    wall_parameters: WallParameters
    parameters: BasePlateParameters
    nano_model: ArduinoNanoCaseModel
    pro_model: ArduinoProMicroCaseModel

    @property
    def dimensions(self) -> list[float]:
        return [
            self.screw_placement_model.body.width,
            self.screw_placement_model.body.depth,
            self.screw_placement_model.bottom_thickness,
        ]

    @property
    def coords(self) -> list[float]:
        return [
            self.screw_placement_model.body.start_x(),
            self.screw_placement_model.body.start_y(),
            -(
                self.body_parameters.height
                + self.screw_placement_model.bottom_thickness
            ),
        ]

    @property
    def screw_head_radius(self) -> float:
        return self.screw_placement_model.screw_head_diameter / 2

    @property
    def screw_head_height(self) -> float:
        return (
            self.screw_placement_model.bottom_thickness
            - self.parameters.screw_height
        )

    @property
    def screw_head_coords(self) -> list[list[float]]:
        coords = []
        for x, y in self.screw_placement_model.get_centered_points():
            coords.append([x, y, self.screw_placement_model.bottom_z])
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
        z = self.screw_placement_model.bottom_z + self.screw_head_height
        for x, y in self.screw_placement_model.get_centered_points():
            coords.append([x, y, z])
        return coords

    @property
    def cavity_dimensions(self) -> list[float]:
        standoff_size = self.screw_placement_model.standoff_size
        return [
            self.dimensions[0] - standoff_size * 2,
            self.screw_placement_model.body.end_y()
            - self.screw_placement_model.body.divider_y
            - standoff_size * 2,
            self.screw_placement_model.bottom_thickness
            - self.wall_parameters.thickness,
        ]

    @property
    def cavity_coords(self) -> list[float]:
        standoff_size = self.screw_placement_model.standoff_size
        return [
            self.coords[0] + standoff_size,
            self.screw_placement_model.body.divider_y + standoff_size,
            self.coords[2] + self.wall_parameters.thickness,
        ]

    @property
    def pro_case_coords(self) -> list[float]:
        pro_y_size = self.pro_model.dimensions[0]
        nano_y_size = self.nano_model.dimensions[0]
        gap = (self.cavity_dimensions[1] - pro_y_size - nano_y_size) / 3.0

        end_x_cavity = self.cavity_coords[0] + self.cavity_dimensions[0]
        x = (
            end_x_cavity
            - self.pro_model.dimensions[1] / 2
            - self.wall_parameters.thickness
        )

        y = self.cavity_coords[1] + gap + nano_y_size + gap + pro_y_size / 2
        z = self.cavity_coords[2] + self.pro_model.dimensions[2] / 2
        return [x, y, z]

    @property
    def nano_case_coords(self) -> list[float]:
        pro_y_size = self.pro_model.dimensions[0]
        nano_y_size = self.nano_model.dimensions[0]
        gap = (self.cavity_dimensions[1] - pro_y_size - nano_y_size) / 3.0

        end_x_cavity = self.cavity_coords[0] + self.cavity_dimensions[0]
        x = (
            end_x_cavity
            - self.nano_model.dimensions[1] / 2
            - self.wall_parameters.thickness
        )

        y = self.cavity_coords[1] + gap + nano_y_size / 2
        z = self.cavity_coords[2] + self.nano_model.dimensions[2] / 2
        return [x, y, z]

    @property
    def cable_path_radius(self) -> float:
        return (
            self.body_parameters.bottom_thickness
            - self.wall_parameters.thickness
        )

    @property
    def cable_path_inner_radius(self) -> float:
        return self.cable_path_radius - self.wall_parameters.thickness

    @property
    def cable_path_height(self) -> float:
        return self.wall_parameters.thickness

    @property
    def cable_path_mask_dimensions(self) -> list[float]:
        return [
            self.cable_path_radius,
            self.cable_path_radius * 2,
            self.cable_path_height,
        ]

    @property
    def cable_path_mask_coords(self) -> list[float]:
        return [-self.cable_path_radius / 2, 0, 0]

    @property
    def cable_path_grid_coords(self) -> list[list[float]]:
        # Calculate Y layout
        count_y = int(self.cavity_dimensions[1] // (self.cable_path_radius * 2))
        if count_y == 0:
            return []

        available_y = self.cavity_dimensions[1] - (
            count_y * self.cable_path_radius * 2
        )
        gap_y = available_y / (count_y + 1)

        y_starts = []
        for i in range(count_y):
            y_starts.append(
                self.cavity_coords[1]
                + gap_y
                + self.cable_path_radius
                + i * (gap_y + self.cable_path_radius * 2)
            )

        # Calculate X layout
        pro_min_x = self.pro_case_coords[0] - self.pro_model.dimensions[1] / 2
        nano_min_x = (
            self.nano_case_coords[0] - self.nano_model.dimensions[1] / 2
        )
        cases_min_x = min(pro_min_x, nano_min_x)

        available_x = cases_min_x - self.cavity_coords[0]
        rows = self.parameters.cable_path_rows

        gap_x = (available_x - rows * self.cable_path_height) / (rows + 1)

        coords = []
        for i in range(rows):
            x = (
                self.cavity_coords[0]
                + gap_x
                + self.cable_path_height / 2
                + i * (gap_x + self.cable_path_height)
            )
            for y in y_starts:
                coords.append([x, y, self.cavity_coords[2]])

        return coords
