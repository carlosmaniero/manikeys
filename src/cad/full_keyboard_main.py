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
class FullKeyboardMain(ManifoldObject):
    model: BodyModel
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y

        height = self.model.sphere.highest + self.parameters.body.height

        mask = manifold3d.Manifold.cube(
            [
                self.model.width,
                self.model.end_y() - divider_y,
                height * 2,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                divider_y,
                -self.parameters.body.height,
            ]
        )

        body = load_stl_to_manifold("build/full_keyboard.stl")

        return body ^ mask


if __name__ == "__main__":
    full_keyboard_main = injector.get(FullKeyboardMain)
    full_keyboard_main.program(sys.argv)
