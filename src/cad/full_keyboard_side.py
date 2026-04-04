from __future__ import annotations
from context import injector
import sys
import manifold3d
from dataclasses import dataclass
from models.body import BodyModel
from models.parameters import Parameters
from injector import inject, singleton
from loader import load_stl_to_manifold
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class FullKeyboardSide(ManifoldObject):
    model: BodyModel
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y

        height = self.model.sphere.highest + self.parameters.body.height

        # Everything where y < divider_y AND x < hand_support_end_x
        mask = manifold3d.Manifold.cube(
            [
                self.model.hand_support_end_x - self.model.start_x(),
                divider_y - self.model.start_y(),
                height * 2,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                self.model.start_y(),
                -self.parameters.body.height,
            ]
        )

        body = load_stl_to_manifold("build/full_keyboard.stl")

        return body ^ mask


if __name__ == "__main__":
    full_keyboard_side = injector.get(FullKeyboardSide)
    full_keyboard_side.program(sys.argv)
