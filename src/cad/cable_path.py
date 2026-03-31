from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.socket_placement import SocketPlacementInner
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class CablePath(OSCObject):
    model: SocketPlacementInner
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        # We want a cylinder that is long enough to pass through the divider
        # and any other walls in its path.

        radius = self.parameters.body.cabe_hole_radius
        thickness = self.parameters.body.thickness
        height = self.parameters.body.height

        # Using a large enough length to ensure it cuts through both sides
        length = 100

        return (
            osc.cylinder(
                r=radius,
                h=length,
                center=True,
            )
            .rotx(90)
            .right(self.model.end_x() - radius - thickness * 3)
            .back(self.model.sphere.start_y())
            .down(height - radius - thickness * 2)
        )


if __name__ == "__main__":
    cable_path = injector.get(CablePath)
    cable_path.program(sys.argv)
