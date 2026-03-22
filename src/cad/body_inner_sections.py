from __future__ import annotations
from context import injector
import sys
import openscad as osc
from dataclasses import dataclass
from models.body import BodyInnerModel
from models.parameters import Parameters
from injector import inject, singleton
from loader import load_stl
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class BodyInnerSections(OSCObject):
    model: BodyInnerModel
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        divider = (
            osc.cube(
                [
                    self.model.width,
                    self.parameters.body.thickness * 2,
                    self.model.hole.outer_highest + self.parameters.body.height,
                ],
            )
            .right(self.model.start_x())
            .down(self.parameters.body.height)
            .back(self.model.hole.outer_start_y())
        )

        cabe_hole_radius = 10

        cabe_hole = (
            osc.cylinder(
                r=cabe_hole_radius,
                h=self.parameters.body.thickness * 2 + 1,
            )
            .rotx(90)
            .right(
                self.model.end_x()
                - cabe_hole_radius
                - self.parameters.body.thickness * 2
            )
            .back(
                self.model.hole.outer_start_y()
                + self.parameters.body.thickness * 2
                + 0.5
            )
            .down(
                self.parameters.body.height
                - cabe_hole_radius
                - self.parameters.body.thickness * 2
            )
        )

        body = load_stl("build/cad/body_inner.stl")

        return body - (divider - cabe_hole)


if __name__ == "__main__":
    bodyInnerSections = injector.get(BodyInnerSections)
    bodyInnerSections.program(sys.argv)
