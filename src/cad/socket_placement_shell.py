from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl
from models.parameters import Parameters
from models.socket_placement import SocketPlacementInner
from models.body import BodyModel
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class SocketPlacementShell(OSCObject):
    model: SocketPlacementInner
    body: BodyModel
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        divider_size = (
            self.parameters.body.thickness * 2
            + self.parameters.body.clearance * 2
        )
        divider_y = self.model.divider_y - divider_size / 2

        body_divider = (
            osc.cube(
                [
                    self.model.width * 3,
                    divider_size,
                    self.model.sphere.highest + self.parameters.body.height,
                ],
            )
            .right(self.model.start_x() - self.model.width)
            .down(self.parameters.body.height)
            .back(divider_y)
        )

        height = self.model.sphere.highest + self.parameters.body.height

        side_divider_size = self.parameters.body.clearance

        side_divider = (
            osc.cube(
                [
                    side_divider_size,
                    self.body.divider_y - self.body.start_y(),
                    height * 2,
                ],
            )
            .right(
                self.body.hand_support_end_x + self.parameters.body.thickness
            )
            .back(self.body.start_y())
            .down(self.parameters.body.height)
        )

        return (
            load_stl("build/cad/socket_placement.stl")
            - load_stl("build/cad/socket_placement_inner_sections.stl")
            - side_divider
            - body_divider
        )


if __name__ == "__main__":
    socket_placement_shell = injector.get(SocketPlacementShell)
    socket_placement_shell.program(sys.argv)
