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
class USBCConnectorMaskCAD(ManifoldObject):
    parameters: Parameters
    model: USBCModel

    @property
    def thickness(self) -> float:
        return self.parameters.body.thickness

    def assemble(self) -> manifold3d.Manifold:
        wall_thickness = self.thickness + self.model.error_margin

        # depth is now along Y
        depth = self.model.connector_depth + wall_thickness
        height = self.model.connector_height + self.model.error_margin * 2
        width = self.model.connector_width + self.model.error_margin * 2

        radius = height / 2

        # Cylinder axis is now along X (width)
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

        # Translate to the +Y edge of the PCB and -Z side
        return manifold3d.Manifold.hull(left_cyl + right_cyl).translate(
            [
                0,
                self.model.pcb_width / 2
                + depth / 2
                - self.model.connector_depth
                + 1.5,
                -self.model.pcb_height / 2 - self.model.connector_height / 2,
            ]
        )


if __name__ == "__main__":
    mask = injector.get(USBCConnectorMaskCAD)
    mask.program(sys.argv)
