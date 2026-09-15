from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from structure.body.models import BodyModel
from structure.body.parameters import BodyParameters
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountShellMainCAD(ManifoldObject):
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
                self.model.bottom_z,
            ]
        )

        shell = self.deps.stls["build/switches/socket/mount/cad/shell.stl"]

        return shell ^ mask


if __name__ == "__main__":
    main = injector.get(MountShellMainCAD)
    main.program(sys.argv)
