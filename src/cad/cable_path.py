from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.socket_placement import SocketPlacementInner
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class CablePath(ManifoldObject):
    model: SocketPlacementInner
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        # We want a cylinder that is long enough to pass through the divider
        # and any other walls in its path.

        radius = self.parameters.body.cabe_hole_radius
        thickness = self.parameters.body.thickness
        height = self.parameters.body.height

        # Using a large enough length to ensure it cuts through both sides
        length = 100

        return (
            manifold3d.Manifold.cylinder(
                radius_low=radius,
                height=length,
                center=True,
            )
            .rotate([90, 0, 0])
            .translate(
                [
                    self.model.end_x() - radius - thickness * 3,
                    self.model.sphere.start_y(),
                    -(height - radius - thickness * 2),
                ]
            )
        )


if __name__ == "__main__":
    cable_path = injector.get(CablePath)
    cable_path.program(sys.argv)
