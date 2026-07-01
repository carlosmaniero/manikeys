from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.body import BodyModel
from models.parameters import Parameters
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class FullKeyboardHandWithSupports(ManifoldObject):
    model: BodyModel
    parameters: Parameters

    def _create_support_y(self, x_pos: float) -> manifold3d.Manifold:
        length = self.model.divider_y - self.model.start_y()
        return manifold3d.Manifold.cube(
            [1.5, length, 1.5],
            center=False,
        ).translate(
            [
                x_pos,
                self.model.start_y(),
                self.model.bottom_z,
            ]
        )

    def _create_support_x(self, y_pos: float) -> manifold3d.Manifold:
        width = self.model.end_x() - self.model.hand_support_end_x
        return manifold3d.Manifold.cube(
            [width, 1.5, 1.5],
            center=False,
        ).translate(
            [
                self.model.hand_support_end_x,
                y_pos,
                self.model.bottom_z,
            ]
        )

    def _create_mask(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y
        height = self.model.sphere.highest + self.parameters.body.height

        return manifold3d.Manifold.cube(
            [
                self.model.end_x() - self.model.hand_support_end_x,
                divider_y - self.model.start_y(),
                height * 2,
            ],
            center=False,
        ).translate(
            [
                self.model.hand_support_end_x,
                self.model.start_y(),
                -self.parameters.body.height,
            ]
        )

    def assemble(self) -> manifold3d.Manifold:
        hand = load_stl_to_manifold("build/cad/full_keyboard_hand.stl")
        inner = load_stl_to_manifold("build/cad/body_inner.stl")
        screw_holes = load_stl_to_manifold("build/cad/body_screw_hole.stl")
        mask = self._create_mask()

        x_range = self.model.end_x() - self.model.hand_support_end_x
        y_range = self.model.divider_y - self.model.start_y()

        num_supports_y = int(x_range / 5)
        num_supports_x = int(y_range / 5)

        supports = manifold3d.Manifold()
        for i in range(num_supports_y):
            x_pos = self.model.hand_support_end_x + x_range * (i + 1) / (
                num_supports_y + 1
            )
            supports += self._create_support_y(x_pos)

        for i in range(num_supports_x):
            y_pos = self.model.start_y() + y_range * (i + 1) / (
                num_supports_x + 1
            )
            supports += self._create_support_x(y_pos)

        support = (supports ^ (inner ^ mask)) - screw_holes

        return hand + support


if __name__ == "__main__":
    hand_with_supports = injector.get(FullKeyboardHandWithSupports)
    hand_with_supports.program(sys.argv)
