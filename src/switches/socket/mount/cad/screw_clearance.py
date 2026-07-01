from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from structure.body.screws.models import ScrewPlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountScrewClearanceCAD(ManifoldObject):
    model: ScrewPlacementModel

    def assemble(self) -> manifold3d.Manifold:
        cubes = []
        for x, y in self.model.get_mask_points():
            cube = manifold3d.Manifold.cube(
                [
                    self.model.mask_size,
                    self.model.mask_size,
                    self.model.mask_height,
                ],
                center=False,
            ).translate([x, y, self.model.mask_z])
            cubes.append(cube)

        return manifold3d.Manifold.batch_boolean(cubes, manifold3d.OpType.Add)


if __name__ == "__main__":
    clearance = injector.get(MountScrewClearanceCAD)
    clearance.program(sys.argv)
