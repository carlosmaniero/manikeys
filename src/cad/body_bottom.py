from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.body_screw_placement import BodyScrewPlacementModel
from models.parameters import Parameters
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class BodyBottomCAD(ManifoldObject):
    model: BodyScrewPlacementModel
    parameters: Parameters

    def screw_head_holes(self) -> manifold3d.Manifold:
        holes = []
        offset = 0.1
        for x, y in self.model.get_centered_points():
            hole = manifold3d.Manifold.cylinder(
                radius_low=self.model.screw_head_diameter / 2,
                height=self.model.screw_head_height + offset,
                circular_segments=100,
                center=False,
            )
            hole = hole.translate([x, y, self.model.screw_head_z - offset / 2])
            holes.append(hole)
        return manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)

    def screw_holes(self) -> manifold3d.Manifold:
        holes = []
        offset = 0.1
        for x, y in self.model.get_centered_points():
            hole = manifold3d.Manifold.cylinder(
                radius_low=self.model.screw_diameter / 2,
                height=self.model.bottom_thickness + offset,
                circular_segments=100,
                center=False,
            )
            hole = hole.translate([x, y, self.model.bottom_z - offset / 2])
            holes.append(hole)
        return manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)

    def assemble(self) -> manifold3d.Manifold:
        bottom = manifold3d.Manifold.cube(
            [
                self.model.body.width,
                self.model.body.depth,
                self.model.bottom_thickness,
            ],
            center=False,
        ).translate(
            [
                self.model.body.start_x(),
                self.model.body.start_y(),
                -(self.parameters.body.height + self.model.bottom_thickness),
            ]
        )

        return bottom - self.screw_holes() - self.screw_head_holes()


if __name__ == "__main__":
    body_bottom = injector.get(BodyBottomCAD)
    body_bottom.program(sys.argv)
