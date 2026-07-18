from globals.wall.parameters import WallParameters
from connectors.usbc.parameters import USBCParameters
from dataclasses import dataclass
from injector import inject, singleton
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class USBCModel:
    wall_parameters: WallParameters
    usbc_parameters: USBCParameters
    body_model: BodyModel

    @property
    def thickness(self) -> float:
        return self.wall_parameters.thickness

    @property
    def width(self) -> float:
        return self.pcb_length + self.thickness * 2

    @property
    def length(self) -> float:
        return self.thickness + self.mounting_hole_diameter + self.thickness

    @property
    def adapter_height(self) -> float:
        return self.thickness + self.pcb_height + self.usbc.height

    @property
    def inner_offset(self) -> float:
        return self.wall_parameters.thickness / 2

    @property
    def body_offset(self) -> list[float]:
        thickness = self.wall_parameters.thickness
        full_length = self.pcb_width + thickness * 2

        max_x = (self.pcb_length + thickness * 2) / 2
        max_y = full_length / 2

        return [
            self.body_model.start_x() + self.wall_parameters.fillet + max_x,
            self.body_model.end_y() - max_y + self.inner_offset,
            self.body_model.bottom_z
            + self.body_model.connectors_bottom_offset
            + self.pcb_height / 2
            + self.connector_height,
        ]

    @property
    def usbc(self) -> USBCParameters:
        return self.usbc_parameters

    @property
    def pcb_width(self) -> float:
        return self.usbc.width

    @property
    def pcb_length(self) -> float:
        return self.usbc.length

    @property
    def pcb_height(self) -> float:
        return self.usbc.pcb_thickness

    @property
    def connector_width(self) -> float:
        return 9.0

    @property
    def connector_height(self) -> float:
        return 3.2

    @property
    def connector_depth(self) -> float:
        return 7.0

    @property
    def error_margin(self) -> float:
        return self.usbc.error_margin

    @property
    def mounting_hole_diameter(self) -> float:
        return 3.0

    @property
    def mounting_hole_radius(self) -> float:
        return self.mounting_hole_diameter / 2

    @property
    def mounting_hole_x(self) -> float:
        return self.pcb_length / 2 - 1.0 - self.mounting_hole_radius

    @property
    def mounting_hole_y(self) -> float:
        return self.pcb_width / 2 - 1.0 - self.mounting_hole_radius
