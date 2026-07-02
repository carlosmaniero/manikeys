from __future__ import annotations
from structure.body.parameters import BodyParameters
from core.context import injector
import sys
import manifold3d
from dataclasses import dataclass
from structure.body.models import BodyModel
from injector import inject, singleton
from core.loader import load_stl_to_manifold
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MainAssemblyCAD(ManifoldObject):
    model: BodyModel
    body_parameters: BodyParameters

    def assemble(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y

        height = self.model.sphere.highest + self.body_parameters.height

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
                -self.body_parameters.height,
            ]
        )

        body = load_stl_to_manifold("build/assembly/cad/full_keyboard.stl")

        return body ^ mask


if __name__ == "__main__":
    main = injector.get(MainAssemblyCAD)
    main.program(sys.argv)
