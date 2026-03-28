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
        divider_size = self.parameters.body.thickness * 2
        divider_y = self.model.divider_y - divider_size / 2

        divider = (
            osc.cube(
                [
                    self.model.width,
                    divider_size,
                    self.model.sphere.highest + self.parameters.body.height,
                ],
            )
            .right(self.model.start_x())
            .down(self.parameters.body.height)
            .back(divider_y)
        )

        cabe_hole = (
            osc.cylinder(
                r=self.parameters.body.cabe_hole_radius,
                h=self.parameters.body.thickness * 2 + 1,
            )
            .rotx(90)
            .right(
                self.model.end_x()
                - self.parameters.body.cabe_hole_radius
                - self.parameters.body.thickness * 2
            )
            .back(
                self.model.sphere.start_y()
                + self.parameters.body.thickness
                + 0.5
            )
            .down(
                self.parameters.body.height
                - self.parameters.body.cabe_hole_radius
                - self.parameters.body.thickness * 2
            )
        )

        body = load_stl("build/cad/body_inner.stl")

        return body - osc.color(divider - cabe_hole, "#00ffffcc")


if __name__ == "__main__":
    bodyInnerSections = injector.get(BodyInnerSections)
    bodyInnerSections.program(sys.argv)
