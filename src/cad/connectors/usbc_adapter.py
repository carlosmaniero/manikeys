from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.parameters import Parameters
from models.usbc import USBCModel
from models.body import BodyModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCAdapterCAD(ManifoldObject):
    parameters: Parameters
    model: USBCModel
    body_model: BodyModel

    @property
    def thickness(self) -> float:
        return self.parameters.body.thickness

    @property
    def width(self) -> float:
        # Long side is now X
        return self.model.pcb_length + self.thickness * 2

    @property
    def length(self) -> float:
        # Wall thickness + Hole diameter + thickness
        # Short side is now Y
        return (
            self.thickness + self.model.mounting_hole_diameter + self.thickness
        )

    @property
    def adapter_height(self) -> float:
        # Ceiling + PCB + Connector space
        return self.thickness + self.model.pcb_height + self.model.usbc.height

    @property
    def main_block(self) -> manifold3d.Manifold:
        # Positioned relative to PCB center (0,0,0)
        # Wall is at +Y (pcb_width/2)
        y_center = self.model.pcb_width / 2 + self.thickness - self.length / 2

        # Top of block is at pcb_height/2 + thickness
        # Bottom of block is at pcb_height/2 + thickness - adapter_height
        z_center = (
            self.model.pcb_height / 2 + self.thickness - self.adapter_height / 2
        )

        return manifold3d.Manifold.cube(
            [
                self.width,
                self.length,
                self.adapter_height,
            ],
            center=True,
        ).translate(
            [
                0,
                y_center,
                z_center,
            ]
        )

    @property
    def body(self) -> manifold3d.Manifold:
        return self.main_block - self.internal_mask - self.connector_mask

    @property
    def internal_mask(self) -> manifold3d.Manifold:
        # Opens bottom, back, and sides by extending the mask.
        # It needs to leave the TOP wall (ceiling) and the front wall (+Y).
        y_start = self.model.pcb_width / 2

        # Mask should leave the top thickness (ceiling)
        # Top of mask = pcb_height/2
        z_mask_top = self.model.pcb_height / 2
        z_mask_center = z_mask_top - self.adapter_height / 2

        mask_length = self.length + self.model.pcb_length
        return manifold3d.Manifold.cube(
            [
                self.width + 0.1,
                mask_length,
                self.adapter_height,
            ],
            center=True,
        ).translate(
            [
                0,
                y_start - mask_length / 2,
                z_mask_center,
            ]
        )

    @property
    def connector_mask(self) -> manifold3d.Manifold:
        return load_stl_to_manifold(
            "build/cad/connectors/usbc_connector_mask.stl"
        )

    @property
    def screw_holes(self) -> manifold3d.Manifold:
        diameter = 1.8
        radius = diameter / 2

        # Tall enough to cut through the ceiling
        height = self.thickness + 5.0
        x_pos = self.model.mounting_hole_x
        y_pos = self.model.mounting_hole_y

        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            circular_segments=60,
            center=True,
        )

        # Positioned in the ceiling
        z_holes = self.model.pcb_height / 2 + self.thickness / 2

        return (
            hole.translate([x_pos, y_pos, 0])
            + hole.translate([-x_pos, y_pos, 0])
        ).translate([0, 0, z_holes])

    def assemble(self) -> manifold3d.Manifold:
        # Align with the same world position as USBCCAD
        return (self.body - self.screw_holes).translate(self.model.body_offset)


if __name__ == "__main__":
    adapter = injector.get(USBCAdapterCAD)
    adapter.program(sys.argv)
