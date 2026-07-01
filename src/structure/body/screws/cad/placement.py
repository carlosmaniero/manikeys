from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from structure.body.screws.models import ScrewPlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class ScrewPlacementCAD(ManifoldObject):
    model: ScrewPlacementModel

    def assemble(self) -> manifold3d.Manifold:
        cubes = []
        for x, y in self.model.points:
            cube = manifold3d.Manifold.cylinder(
                self.model.cube_height,
                self.model.cube_size / 2,
                center=True,
            ).translate(
                [
                    x + self.model.cube_size / 2,
                    y + self.model.cube_size / 2,
                    self.model.z,
                ]
            )
            cubes.append(cube)

        body = load_stl_to_manifold("build/structure/body/shape.stl")

        return (
            manifold3d.Manifold.batch_boolean(cubes, manifold3d.OpType.Add)
            ^ body
        )


if __name__ == "__main__":
    placement = injector.get(ScrewPlacementCAD)
    placement.program(sys.argv)
