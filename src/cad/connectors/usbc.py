from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.usbc import USBCModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCCAD(ManifoldObject):
    parameters: Parameters
    model: USBCModel

    @property
    def pcb(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.pcb_width,
                self.model.pcb_length,
                self.model.pcb_height,
            ],
            center=True,
        )

    @property
    def connector(self) -> manifold3d.Manifold:
        depth = 7.0
        height = 3.2
        width = 9.0
        radius = height / 2
        cylinder = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=depth,
            center=True,
            circular_segments=60,
        ).rotate([0, 90, 0])
        y_offset = (width / 2) - radius
        left_cyl = cylinder.translate([0, -y_offset, 0])
        right_cyl = cylinder.translate([0, y_offset, 0])
        return manifold3d.Manifold.hull(left_cyl + right_cyl).translate(
            [
                -self.model.pcb_width / 2 + depth / 2 - 1.5,
                0,
                self.model.pcb_height / 2 + height / 2,
            ]
        )

    @property
    def mounting_holes(self) -> manifold3d.Manifold:
        diameter = 3.0
        radius = diameter / 2
        x_pos = -self.model.pcb_width / 2 + 1.0 + radius
        y_pos = self.model.pcb_length / 2 - 1.0 - radius
        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=self.model.pcb_height + 0.2,
            circular_segments=60,
            center=True,
        )
        return hole.translate([x_pos, y_pos, 0]) + hole.translate(
            [x_pos, -y_pos, 0]
        )

    def assemble(self) -> manifold3d.Manifold:
        return self.pcb + self.connector - self.mounting_holes


if __name__ == "__main__":
    adapter = injector.get(USBCCAD)
    adapter.program(sys.argv)
