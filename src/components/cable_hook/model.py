from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton
from components.cable_hook.parameters import CableHookParameters
from models.parameters import SwitchesParameters
from globals.wall.parameters import WallParameters


@singleton
@inject
@dataclass
class CableHookModel:
    parameters: CableHookParameters
    switches_parameters: SwitchesParameters
    wall_parameters: WallParameters

    @property
    def cable_radius(self) -> float:
        return self.switches_parameters.cable_radius

    @property
    def outer_radius(self) -> float:
        return self.cable_radius + self.parameters.wall_thickness

    @property
    def offset_x(self) -> float:
        return self.wall_parameters.thickness
