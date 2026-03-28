from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl
from models.parameters import Parameters
from models.socket_placement import SocketPlacementInner
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class SocketPlacementShell(OSCObject):
    model: SocketPlacementInner
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        body_divider = (
            osc.cube(
                [
                    self.model.width * 3,
                    self.parameters.body.thickness * 2
                    + self.parameters.body.clearance * 2,
                    self.model.sphere.highest + self.parameters.body.height,
                ],
            )
            .right(self.model.start_x() - self.model.width)
            .down(self.parameters.body.height)
            .back(
                self.model.sphere.start_y()
                - self.parameters.body.thickness
                - self.parameters.body.clearance
            )
        )

        return (
            load_stl("build/cad/socket_placement.stl")
            - load_stl("build/cad/socket_placement_inner_sections.stl")
            - body_divider
        )


if __name__ == "__main__":
    socket_placement_shell = injector.get(SocketPlacementShell)
    socket_placement_shell.program(sys.argv)
