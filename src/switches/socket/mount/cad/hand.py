from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from structure.body.models import BodyModel
from structure.body.parameters import BodyParameters
from globals.wall.parameters import WallParameters
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountShellHandCAD(ManifoldObject):
    model: BodyModel
    body_parameters: BodyParameters
    wall_parameters: WallParameters

    def assemble(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y

        height = self.model.sphere.highest + self.body_parameters.height

        start_x = (
            self.model.hand_support_end_x + self.wall_parameters.thickness * 2
        )
        width = self.model.end_x() - start_x

        mask = manifold3d.Manifold.cube(
            [
                width,
                divider_y - self.model.start_y(),
                height * 2,
            ],
            center=False,
        ).translate(
            [
                start_x,
                self.model.start_y(),
                self.model.bottom_z,
            ]
        )

        shell = self.deps.stls["build/switches/socket/mount/cad/shell.stl"]

        return shell ^ mask


if __name__ == "__main__":
    hand = injector.get(MountShellHandCAD)
    hand.program(sys.argv)
