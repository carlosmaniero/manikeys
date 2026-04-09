from dataclasses import dataclass
from injector import inject, singleton
from .parameters import Parameters, USBCParameters


@singleton
@inject
@dataclass
class USBCModel:
    parameters: Parameters

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
