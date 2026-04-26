from dataclasses import dataclass
from injector import inject, singleton
from .parameters import Parameters
from .body import BodyModel
import numpy as np


@singleton
@inject
@dataclass
class MagnetSnapModel:
    model: BodyModel
    parameters: Parameters

    @property
    def thickness(self) -> float:
        return self.parameters.body.thickness

    @property
    def magnet_height(self) -> float:
        return self.parameters.magnet.height

    @property
    def magnet_diameter(self) -> float:
        return self.parameters.magnet.diameter

    @property
    def full_magnet_height(self) -> float:
        return (
            self.parameters.magnet.height + self.parameters.magnet.error_margin
        )

    def _get_z_positions(self, x: float, y: float) -> tuple[float, float]:
        top_z = self.model.sphere.z(
            np.array([x]), np.array([y]), -self.thickness * 3
        )[0]
        bottom_z = self.model.bottom_z + self.thickness * 2
        return top_z, bottom_z

    def get_main_hand_positions(self) -> list[list[float]]:
        divider_y = self.model.divider_y
        x_start = self.model.hand_support_end_x
        x_end = self.model.end_x()

        x_positions = [
            x_start + self.thickness * 4,
            x_end - self.thickness * 4,
        ]

        positions = []

        for x in x_positions:
            top_z, bottom_z = self._get_z_positions(x, divider_y)
            y_offset = self.full_magnet_height / 2

            positions.append([x, divider_y + y_offset, top_z])
            positions.append([x, divider_y - y_offset, top_z])

            positions.append([x, divider_y + y_offset, bottom_z])
            positions.append([x, divider_y - y_offset, bottom_z])

        return positions

    def get_main_side_positions(self) -> list[list[float]]:
        divider_y = self.model.divider_y
        x_start = self.model.start_x()
        x_end = self.model.hand_support_end_x

        x_positions = [
            x_start + self.thickness * 2,
            x_end - self.thickness * 2,
        ]

        positions = []
        for x in x_positions:
            top_z, bottom_z = self._get_z_positions(x, divider_y)
            y_offset = self.full_magnet_height / 2

            positions.append([x, divider_y + y_offset, top_z])  # Main side
            positions.append([x, divider_y - y_offset, top_z])  # Side side

            positions.append([x, divider_y + y_offset, bottom_z])  # Main side
            positions.append([x, divider_y - y_offset, bottom_z])  # Side side

        return positions

    def get_all_positions(self) -> list[list[float]]:
        return self.get_main_hand_positions() + self.get_main_side_positions()
