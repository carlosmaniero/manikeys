from __future__ import annotations
import sys
import os
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl
from models.body_screw_placement import BodyScrewPlacementModel
from models.parameters import Parameters
from openscad_ext.object import OSCObject

DEBUG = os.getenv("DEBUG", "false") == "true"


@singleton
@inject
@dataclass
class BodyBottomCAD(OSCObject):
    model: BodyScrewPlacementModel
    parameters: Parameters

    def screw_head_holes(self) -> osc.PyOpenSCAD:
        holes = []
        offset = 0.1
        for x, y in self.model.get_centered_points():
            hole = osc.cylinder(
                r=self.model.screw_head_diameter / 2,
                h=self.model.screw_head_height + offset,
                center=False,
                fn=100,
            )
            hole = osc.translate(
                hole, [x, y, self.model.screw_head_z - offset / 2]
            )
            holes.append(hole)
        return osc.union(*holes)

    def screw_holes(self) -> osc.PyOpenSCAD:
        holes = []
        offset = 0.1
        for x, y in self.model.get_centered_points():
            hole = osc.cylinder(
                r=self.model.screw_diameter / 2,
                h=self.model.bottom_thickness + offset,
                center=False,
                fn=100,
            )
            hole = osc.translate(hole, [x, y, self.model.bottom_z - offset / 2])
            holes.append(hole)
        return osc.union(*holes)

    def assemble(self) -> osc.PyOpenSCAD:
        bottom = (
            osc.cube(
                [
                    self.model.body.width,
                    self.model.body.depth,
                    self.model.bottom_thickness,
                ],
                center=False,
            )
            .right(self.model.body.start_x())
            .back(self.model.body.start_y())
            .down(self.parameters.body.height + self.model.bottom_thickness)
        )

        return bottom - self.screw_holes() - self.screw_head_holes()

    def show(self):
        bottom = self.assemble()

        if DEBUG:
            body = load_stl("build/cad/body.stl")
            body.color("red", 0.3).show()

        bottom.color("green", 0.7).show()


if __name__ == "__main__":
    body_bottom = injector.get(BodyBottomCAD)
    body_bottom.program(sys.argv)
