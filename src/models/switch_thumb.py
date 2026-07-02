from globals.wall.parameters import WallParameters
from models.parameters import SwitchesParameters
from dataclasses import dataclass

from injector import inject, singleton

from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class SwitchThumbModel:
    body_model: BodyModel
    wall_parameters: WallParameters
    switches_parameters: SwitchesParameters

    def get_positions(self) -> list[list[float]]:
        pos1 = [
            self.body_model.end_x()
            - self.switches_parameters.full_offset
            - self.wall_parameters.thickness * 3,
            self.body_model.divider_y
            - self.switches_parameters.full_offset
            - self.wall_parameters.thickness,
            self.body_model.sphere.highest,
        ]

        pos2 = [
            pos1[0],
            pos1[1] - self.switches_parameters.next_offset,
            pos1[2],
        ]

        pos3 = [
            pos1[0],
            pos2[1] - self.switches_parameters.next_offset,
            pos1[2],
        ]

        return [pos1, pos2, pos3]
