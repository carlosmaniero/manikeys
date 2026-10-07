from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from switches.socket.mount.models import PcbShellHandModel
from switches.socket.mount.parameters import MountScrewHoleParameters
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountScrewHoleHandCAD(ManifoldObject):
    model: PcbShellHandModel
    screw_hole_parameters: MountScrewHoleParameters

    def assemble(self) -> manifold3d.Manifold:
        screw_holes = []
        hole_radius = self.model.mount_model.screw_parameters.m2_diameter / 2
        hole_height = self.screw_hole_parameters.height

        head_radius = (
            self.model.mount_model.screw_parameters.m2_head_diameter / 2
        )
        head_height = self.model.mount_model.screw_parameters.m2_head_height

        for x, y, z, rot in self.model.screw_hole_placements:
            hole = manifold3d.Manifold.cylinder(
                height=hole_height,
                radius_low=hole_radius,
                circular_segments=100,
                center=False,
            )
            head_pocket = manifold3d.Manifold.cylinder(
                height=head_height,
                radius_low=head_radius,
                circular_segments=100,
                center=False,
            ).translate([0, 0, -head_height / 2])

            full_hole = (hole + head_pocket).rotate(rot).translate([x, y, z])
            screw_holes.append(full_hole)

        return manifold3d.Manifold.batch_boolean(
            screw_holes, manifold3d.OpType.Add
        ).translate([0, 0, self.screw_hole_parameters.hand_offset_z])


if __name__ == "__main__":
    screw_hole_hand = injector.get(MountScrewHoleHandCAD)
    screw_hole_hand.program(sys.argv)
