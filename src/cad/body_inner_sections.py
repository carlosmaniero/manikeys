from __future__ import annotations
from context import injector
import sys
import openscad as osc
from dataclasses import dataclass
from models.body import BodyInnerModel, BodyModel
from models.parameters import Parameters
from injector import inject, singleton
from loader import load_stl
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class BodyInnerSections(OSCObject):
    model: BodyInnerModel
    body: BodyModel
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

        height = self.model.sphere.highest + self.parameters.body.height

        side_mask = (
            osc.cube(
                [
                    self.body.hand_support_end_x
                    - self.body.start_x()
                    + self.parameters.body.thickness,
                    self.body.divider_y - self.body.start_y(),
                    height * 2,
                ],
            )
            .right(self.body.start_x())
            .back(self.body.start_y())
            .down(self.parameters.body.height)
        )

        body = load_stl("build/cad/body_inner.stl") - side_mask

        return body - divider


if __name__ == "__main__":
    bodyInnerSections = injector.get(BodyInnerSections)
    bodyInnerSections.program(sys.argv)
