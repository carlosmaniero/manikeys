from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from switches.socket.mount.models import MountModel
from switches.socket.mount.parameters import MountScrewHoleParameters
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountScrewHoleMainCAD(ManifoldObject):
    mount_model: MountModel
    screw_hole_parameters: MountScrewHoleParameters

    def assemble(self) -> manifold3d.Manifold:
        screw_holes = []
        hole_radius = self.mount_model.screw_parameters.m2_diameter / 2
        hole_height = self.screw_hole_parameters.height
        for x, y, z, rot in self.mount_model.screw_hole_placements:
            hole = (
                manifold3d.Manifold.cylinder(
                    height=hole_height,
                    radius_low=hole_radius,
                    circular_segments=100,
                    center=False,
                )
                .rotate(rot)
                .translate([x, y, z])
            )
            screw_holes.append(hole)

        return manifold3d.Manifold.batch_boolean(
            screw_holes, manifold3d.OpType.Add
        ).translate([0, 0, self.screw_hole_parameters.offset_z])


if __name__ == "__main__":
    screw_hole_main = injector.get(MountScrewHoleMainCAD)
    screw_hole_main.program(sys.argv)
