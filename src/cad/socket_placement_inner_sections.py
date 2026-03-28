from __future__ import annotations
from context import injector
import sys
import openscad as osc
from dataclasses import dataclass
from models.socket_placement import SocketPlacementInner
from models.parameters import Parameters
from injector import inject, singleton
from loader import load_stl
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class SocketPlacementInnerSections(OSCObject):
    model: SocketPlacementInner
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        divider_y = (
            self.model.sphere.start_y() - self.parameters.body.thickness * 2
        )
        height = self.model.sphere.highest + self.parameters.body.height

        divider = (
            osc.cube(
                [
                    self.model.width,
                    self.parameters.body.thickness * 4,
                    height,
                ],
            )
            .right(self.model.start_x())
            .down(self.parameters.body.height)
            .back(divider_y)
        )

        side_section = (
            osc.cube(
                [
                    self.model.hand_support_end_x
                    - self.model.hand_support_start_x,
                    divider_y - self.model.start_y(),
                    height,
                ],
            )
            .right(self.model.start_x())
            .back(self.model.start_y())
            .down(self.parameters.body.height)
        )

        cabe_hole = (
            osc.cylinder(
                r=self.parameters.body.cabe_hole_radius,
                h=self.parameters.body.thickness * 4 + 1,
            )
            .rotx(90)
            .right(
                self.model.end_x()
                - self.parameters.body.cabe_hole_radius
                - self.parameters.body.thickness * 4
            )
            .back(
                self.model.sphere.start_y()
                + self.parameters.body.thickness * 2
                + 0.5
            )
            .down(
                self.parameters.body.height
                - self.parameters.body.cabe_hole_radius
                - self.parameters.body.thickness * 4
            )
        )

        body = load_stl("build/cad/socket_placement_inner.stl")

        return body - osc.color(
            (divider | side_section) - cabe_hole, "#00ffffcc"
        )


if __name__ == "__main__":
    socketPlacementInnerSections = injector.get(SocketPlacementInnerSections)
    socketPlacementInnerSections.program(sys.argv)
