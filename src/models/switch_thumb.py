from dataclasses import dataclass

from injector import inject, singleton

from structure.body.models import BodyModel
from .parameters import Parameters


@singleton
@inject
@dataclass
class SwitchThumbModel:
    body_model: BodyModel
    parameters: Parameters

    def get_positions(self) -> list[list[float]]:
        pos1 = [
            self.body_model.end_x()
            - self.parameters.switches.full_offset
            - self.parameters.wall.thickness * 3,
            self.body_model.divider_y
            - self.parameters.switches.full_offset
            - self.parameters.wall.thickness,
            self.body_model.sphere.highest,
        ]

        pos2 = [
            pos1[0],
            pos1[1] - self.parameters.switches.next_offset,
            pos1[2],
        ]

        pos3 = [
            pos1[0],
            pos2[1] - self.parameters.switches.next_offset,
            pos1[2],
        ]

        return [pos1, pos2, pos3]
