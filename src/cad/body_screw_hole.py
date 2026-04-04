from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.body_screw_placement import BodyScrewPlacementModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class BodyScrewHoleCAD(ManifoldObject):
    model: BodyScrewPlacementModel

    def assemble(self) -> manifold3d.Manifold:
        holes = []
        offset = 0.1
        for x, y in self.model.get_centered_points():
            hole = manifold3d.Manifold.cylinder(
                radius_low=self.model.screw_diameter / 2,
                height=self.model.screw_height + offset,
                circular_segments=100,
                center=False,
            )
            hole = hole.translate([x, y, self.model.screw_z - offset / 2])
            holes.append(hole)

        return manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)


if __name__ == "__main__":
    body_screw_hole = injector.get(BodyScrewHoleCAD)
    body_screw_hole.program(sys.argv)
