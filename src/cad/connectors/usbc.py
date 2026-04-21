from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.usbc import USBCModel
from models.body import BodyModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCCAD(ManifoldObject):
    parameters: Parameters
    model: USBCModel
    body_model: BodyModel

    @property
    def pcb(self) -> manifold3d.Manifold:
        # Long side is now X
        return manifold3d.Manifold.cube(
            [
                self.model.pcb_length,
                self.model.pcb_width,
                self.model.pcb_height,
            ],
            center=True,
        )

    @property
    def connector(self) -> manifold3d.Manifold:
        # depth is now along Y
        depth = self.model.connector_depth
        height = self.model.connector_height
        width = self.model.connector_width
        radius = height / 2

        # Cylinder axis along X (width)
        cylinder = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=depth,
            center=True,
            circular_segments=60,
        ).rotate([90, 0, 0])

        x_offset = (width / 2) - radius
        left_cyl = cylinder.translate([-x_offset, 0, 0])
        right_cyl = cylinder.translate([x_offset, 0, 0])

        return manifold3d.Manifold.hull(left_cyl + right_cyl).translate(
            [
                0,
                self.model.pcb_width / 2 - depth / 2 + 1.5,
                self.model.pcb_height / 2 + height / 2,
            ]
        )

    @property
    def mounting_holes(self) -> manifold3d.Manifold:
        radius = self.model.mounting_hole_radius
        x_pos = self.model.mounting_hole_x
        y_pos = self.model.mounting_hole_y
        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=self.model.pcb_height + 0.2,
            circular_segments=60,
            center=True,
        )
        # Symmetric in X
        return hole.translate([x_pos, y_pos, 0]) + hole.translate(
            [-x_pos, y_pos, 0]
        )

    def assemble(self) -> manifold3d.Manifold:
        return (self.pcb + self.connector - self.mounting_holes).translate(
            self.model.body_offset
        )


if __name__ == "__main__":
    adapter = injector.get(USBCCAD)
    adapter.program(sys.argv)
