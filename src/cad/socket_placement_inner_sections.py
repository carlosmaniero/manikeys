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
        divider_size = (
            self.parameters.body.thickness * 4
            + self.parameters.body.clearance * 2
        )
        divider_y = self.model.divider_y - divider_size / 2

        height = self.model.sphere.highest + self.parameters.body.height

        divider = (
            osc.cube(
                [
                    self.model.width,
                    divider_size,
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
                h=divider_size + 1,
            )
            .rotx(90)
            .right(
                self.model.end_x()
                - self.parameters.body.cabe_hole_radius
                - self.parameters.body.thickness * 4
            )
            .back(divider_y + divider_size + 0.5)
            .down(
                self.parameters.body.height
                - self.parameters.body.cabe_hole_radius
                - self.parameters.body.thickness * 4
            )
        )

        body = load_stl("build/cad/socket_placement_inner.stl")

        return body - ((divider | side_section) - cabe_hole)


if __name__ == "__main__":
    socketPlacementInnerSections = injector.get(SocketPlacementInnerSections)
    socketPlacementInnerSections.program(sys.argv)
