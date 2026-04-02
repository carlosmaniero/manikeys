from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.body_screw_placement import BodyScrewPlacementModel
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class BodyScrewHoleCAD(OSCObject):
    model: BodyScrewPlacementModel

    def assemble(self) -> osc.PyOpenSCAD:
        holes = []
        offset = 0.1
        for x, y in self.model.get_centered_points():
            hole = osc.cylinder(
                r=self.model.screw_diameter / 2,
                h=self.model.screw_height + offset,
                center=False,
                fn=100,
            )
            hole = osc.translate(hole, [x, y, self.model.screw_z - offset / 2])
            holes.append(hole)

        return osc.union(*holes)


if __name__ == "__main__":
    body_screw_hole = injector.get(BodyScrewHoleCAD)
    body_screw_hole.program(sys.argv)
