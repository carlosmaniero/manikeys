from dataclasses import dataclass

from injector import inject, singleton

from .body import BodyModel
from .parameters import Parameters


@singleton
@inject
@dataclass
class CapThumbModel:
    body_model: BodyModel
    parameters: Parameters

    def get_positions(self) -> list[list[float]]:
        pos1 = [
            self.body_model.caps_bottom_sphere.highest_x,
            self.body_model.caps_bottom_sphere.start_y()
            - self.parameters.caps.full_offset,
            self.body_model.caps_bottom_sphere.highest,
        ]

        pos2 = [
            pos1[0],
            pos1[1] - self.parameters.caps.next_offset,
            pos1[2],
        ]

        pos3 = [
            pos1[0],
            pos2[1] - self.parameters.caps.next_offset,
            pos1[2],
        ]

        return [pos1, pos2, pos3]
