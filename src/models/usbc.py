from dataclasses import dataclass
from injector import inject, singleton
from .parameters import Parameters, USBCParameters
from .body import BodyModel


@singleton
@inject
@dataclass
class USBCModel:
    parameters: Parameters
    body_model: BodyModel

    @property
    def body_offset(self) -> list[float]:
        # Centering logic for the new orientation (long side is X)
        thickness = self.parameters.body.thickness
        # Now Y is the short side (pcb_width)
        full_length = self.pcb_width + thickness * 2

        max_x = (self.pcb_length + thickness * 2) / 2
        max_y = full_length / 2

        return [
            self.body_model.start_x() + self.parameters.body.fillet + max_x,
            self.body_model.end_y() - max_y,
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
        # Long side (X) symmetry
        return self.pcb_length / 2 - 1.0 - self.mounting_hole_radius

    @property
    def mounting_hole_y(self) -> float:
        # Near the connector (Y side)
        return self.pcb_width / 2 - 1.0 - self.mounting_hole_radius
