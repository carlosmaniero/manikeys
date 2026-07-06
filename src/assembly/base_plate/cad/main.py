from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton

from core.context import injector
from core.loader import load_stl_to_manifold
from core.manifold_ext.object import ManifoldObject
from structure.body.models import BodyModel
from assembly.base_plate.model import BasePlateModel


@singleton
@inject
@dataclass
class BasePlateMainCAD(ManifoldObject):
    model: BodyModel
    base_plate_model: BasePlateModel

    def assemble(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y

        mask_height = self.base_plate_model.dimensions[2] + 20

        mask = manifold3d.Manifold.cube(
            [
                self.model.width,
                self.model.end_y() - divider_y,
                mask_height,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                divider_y,
                self.base_plate_model.coords[2] - 10,
            ]
        )

        base_plate = load_stl_to_manifold(
            "build/assembly/base_plate/cad/base_plate.stl"
        )

        return base_plate ^ mask


if __name__ == "__main__":
    main = injector.get(BasePlateMainCAD)
    main.program(sys.argv)
