from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from switches.socket.mount.models import MountScrewCylinderModel


@singleton
@inject
@dataclass
class MountPcbsPlacementScrewsCAD(ManifoldObject):
    screw_cylinder_model: MountScrewCylinderModel

    def assemble(self) -> manifold3d.Manifold:
        shape = self.deps.stls["build/structure/body/cad/shape.stl"]

        base_cylinder = manifold3d.Manifold.cylinder(
            self.screw_cylinder_model.height,
            self.screw_cylinder_model.radius,
            circular_segments=100,
            center=False,
        )
        base_cube = manifold3d.Manifold.cube(
            [
                self.screw_cylinder_model.radius,
                self.screw_cylinder_model.radius,
                self.screw_cylinder_model.height,
            ],
            center=False,
        )
        base_quarter = base_cylinder ^ base_cube

        screw_cylinders = []
        for (
            center_x,
            center_y,
            rotation_deg,
        ) in self.screw_cylinder_model.placements:
            cylinder = base_quarter.rotate([0, 0, rotation_deg]).translate(
                [
                    center_x,
                    center_y,
                    self.screw_cylinder_model.z,
                ]
            )
            screw_cylinders.append(cylinder)

        hole_cylinders = []
        for hx, hy in self.screw_cylinder_model.hole_placements:
            hole_cyl = manifold3d.Manifold.cylinder(
                self.screw_cylinder_model.height * 3,
                self.screw_cylinder_model.hole_radius,
                circular_segments=100,
                center=True,
            ).translate(
                [
                    hx,
                    hy,
                    self.screw_cylinder_model.z
                    + self.screw_cylinder_model.height / 2,
                ]
            )
            hole_cylinders.append(hole_cyl)

        main_screw_holes = manifold3d.Manifold.batch_boolean(
            hole_cylinders, manifold3d.OpType.Add
        )

        screws = (
            manifold3d.Manifold.batch_boolean(
                screw_cylinders, manifold3d.OpType.Add
            )
            - main_screw_holes
        )

        return screws ^ shape


if __name__ == "__main__":
    pcbs_placement_screws = injector.get(MountPcbsPlacementScrewsCAD)
    pcbs_placement_screws.program(sys.argv)
