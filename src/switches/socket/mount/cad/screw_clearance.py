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
        clearances = []
        for x, y in self.model.get_centered_points():
            clearance = manifold3d.Manifold.cylinder(
                self.model.mask_height,
                self.model.mask_size / 2,
                circular_segments=100,
                center=False,
            ).translate([x, y, self.model.mask_z])
            clearances.append(clearance)

        return manifold3d.Manifold.batch_boolean(
            clearances, manifold3d.OpType.Add
        )


if __name__ == "__main__":
    clearance = injector.get(MountScrewClearanceCAD)
    clearance.program(sys.argv)
