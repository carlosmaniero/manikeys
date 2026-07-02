from dataclasses import dataclass
from injector import inject, singleton
from models.parameters import Parameters
from connectors.usbc.parameters import USBCParameters
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class USBCModel:
    parameters: Parameters
    body_model: BodyModel

    @property
    def thickness(self) -> float:
        return self.parameters.wall.thickness

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
        return self.parameters.wall.thickness / 2

    @property
    def body_offset(self) -> list[float]:
        thickness = self.parameters.wall.thickness
        full_length = self.pcb_width + thickness * 2

        max_x = (self.pcb_length + thickness * 2) / 2
        max_y = full_length / 2

        return [
            self.body_model.start_x() + self.parameters.wall.fillet + max_x,
            self.body_model.end_y() - max_y + self.inner_offset,
            self.body_model.bottom_z + self.usbc.height + self.pcb_height / 2,
        ]

    @property
    def usbc(self) -> USBCParameters:
        return self.parameters.usbc

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
