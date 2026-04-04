from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.body_screw_placement import BodyScrewPlacementModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class BodyScrewPlacementCAD(ManifoldObject):
    model: BodyScrewPlacementModel

    def assemble(self) -> manifold3d.Manifold:
        cubes = []
        for x, y in self.model.points:
            cube = manifold3d.Manifold.cube(
                [
                    self.model.cube_size,
                    self.model.cube_size,
                    self.model.cube_height,
                ],
                center=False,
            ).translate([x, y, self.model.z])
            cubes.append(cube)

        body = load_stl_to_manifold("build/cad/body.stl")

        return (
            manifold3d.Manifold.batch_boolean(cubes, manifold3d.OpType.Add)
            ^ body
        )


if __name__ == "__main__":
    body_screw_placement = injector.get(BodyScrewPlacementCAD)
    body_screw_placement.program(sys.argv)
