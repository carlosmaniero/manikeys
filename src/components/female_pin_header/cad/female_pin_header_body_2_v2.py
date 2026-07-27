from __future__ import annotations
from dataclasses import dataclass
import sys

from injector import inject, singleton
from manifold3d import Manifold as M

from components.female_pin_header.model import FemalePinHeaderModel
from core.context import injector
from core.manifold_ext.helpers import extrude
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class FemalePinHeaderBody2V2CAD(ManifoldObject):
    model: FemalePinHeaderModel

    @property
    def pocket_body(self) -> M:
        return extrude(
            self.model.pocket_pins_points,
            self.model.pocket_length(2),
        ).translate(
            [
                0,
                0,
                (self.model.outer_length(2) - self.model.pocket_length(2)) / 2,
            ]
        )

    @property
    def pocket_pins(self) -> M:
        return extrude(
            self.model.pocket_pins_points,
            self.model.pin_length(2),
        ).translate(
            [
                0,
                0,
                (self.model.outer_length(2) - self.model.pin_length(2)) / 2,
            ]
        )

    @property
    def main_body(self) -> M:
        return extrude(self.model.full_body_points, self.model.outer_length(2))

    @property
    def wire_paths(self) -> M:
        d = self.model.parameters.wire_diameter
        pitch = self.model.parameters.pitch
        height = self.model.top_left_y

        cube = M.cube([d, height + 2.0, d], center=True)

        z_center = self.model.outer_length(2) / 2

        w1 = cube.translate(
            [
                self.model.wire_path_x,
                self.model.wire_path_y,
                z_center - pitch / 2,
            ]
        )
        w2 = cube.translate(
            [
                self.model.wire_path_x,
                self.model.wire_path_y,
                z_center + pitch / 2,
            ]
        )

        return w1 + w2

    def assemble(self) -> M:
        return (
            self.main_body
            - self.pocket_body
            - self.pocket_pins
            - self.wire_paths
        ).rotate([90, 0, 0])


if __name__ == "__main__":
    female_pin_header_body_2_v2 = injector.get(FemalePinHeaderBody2V2CAD)
    female_pin_header_body_2_v2.program(sys.argv)
