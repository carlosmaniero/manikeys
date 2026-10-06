from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton

from core.context import injector
from core.manifold_ext.object import ManifoldObject
from structure.body.models import BodyModel
from assembly.base_plate.model import BasePlateModel


@singleton
@inject
@dataclass
class BasePlateHandCAD(ManifoldObject):
    model: BodyModel
    base_plate_model: BasePlateModel

    def assemble(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y

        mask_height = self.base_plate_model.dimensions[2] + 20

        mask = manifold3d.Manifold.cube(
            [
                self.model.end_x() - self.model.hand_support_end_x,
                divider_y - self.model.start_y(),
                mask_height,
            ],
            center=False,
        ).translate(
            [
                self.model.hand_support_end_x,
                self.model.start_y(),
                self.base_plate_model.coords[2] - 10,
            ]
        )

        base_plate = self.deps.stls[
            "build/assembly/base_plate/cad/base_plate.stl"
        ]

        return base_plate ^ mask


if __name__ == "__main__":
    hand = injector.get(BasePlateHandCAD)
    hand.program(sys.argv)
