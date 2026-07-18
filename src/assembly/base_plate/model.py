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
            self.screw_placement_model.body.width
            - self.wall_parameters.thickness * 2
            - self.parameters.clearance * 2,
            self.screw_placement_model.body.depth
            - self.wall_parameters.thickness * 2
            - self.parameters.clearance * 2,
            self.parameters.thickness,
        ]

    @property
    def coords(self) -> list[float]:
        return [
            self.screw_placement_model.body.start_x()
            + self.wall_parameters.thickness
            + self.parameters.clearance,
            self.screw_placement_model.body.start_y()
            + self.wall_parameters.thickness
            + self.parameters.clearance,
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
        return self.parameters.thickness - self.parameters.screw_height

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
    def pro_case_coords(self) -> list[float]:
        pro_y_size = self.pro_model.dimensions[0]
        nano_y_size = self.nano_model.dimensions[0]

        standoff_size = self.screw_placement_model.standoff_size
        start_y = self.screw_placement_model.body.divider_y + standoff_size
        end_y = self.screw_placement_model.body.end_y() - standoff_size
        available_depth = end_y - start_y
        gap = (available_depth - pro_y_size - nano_y_size) / 3.0

        end_x = self.coords[0] + self.dimensions[0]
        x = (
            end_x
            - self.pro_model.dimensions[1] / 2
            - self.wall_parameters.thickness
        )

        y = start_y + gap + nano_y_size + gap + pro_y_size / 2
        z = (
            self.coords[2]
            + self.parameters.thickness
            + self.pro_model.dimensions[2] / 2
        )
        return [x, y, z]

    @property
    def nano_case_coords(self) -> list[float]:
        pro_y_size = self.pro_model.dimensions[0]
        nano_y_size = self.nano_model.dimensions[0]

        standoff_size = self.screw_placement_model.standoff_size
        start_y = self.screw_placement_model.body.divider_y + standoff_size
        end_y = self.screw_placement_model.body.end_y() - standoff_size
        available_depth = end_y - start_y
        gap = (available_depth - pro_y_size - nano_y_size) / 3.0

        end_x = self.coords[0] + self.dimensions[0]
        x = (
            end_x
            - self.nano_model.dimensions[1] / 2
            - self.wall_parameters.thickness
        )

        y = start_y + gap + nano_y_size / 2
        z = (
            self.coords[2]
            + self.parameters.thickness
            + self.nano_model.dimensions[2] / 2
        )
        return [x, y, z]

    @property
    def mask_dimensions(self) -> list[float]:
        return [
            self.screw_placement_model.body.width
            - self.wall_parameters.thickness * 2,
            self.screw_placement_model.body.depth
            - self.wall_parameters.thickness * 2,
            self.parameters.thickness + 2.0,
        ]

    @property
    def mask_coords(self) -> list[float]:
        return [
            self.screw_placement_model.body.start_x()
            + self.wall_parameters.thickness,
            self.screw_placement_model.body.start_y()
            + self.wall_parameters.thickness,
            -(
                self.body_parameters.height
                + self.screw_placement_model.bottom_thickness
                + 1.0
            ),
        ]
