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

        return self.model.pcb_length + self.thickness * 2

    @property
    def length(self) -> float:

        return (
            self.thickness + self.model.mounting_hole_diameter + self.thickness
        )

    @property
    def adapter_height(self) -> float:
        return self.model.usbc.height + self.thickness * 2

    @property
    def main_block(self) -> manifold3d.Manifold:

        y_center = self.model.pcb_width / 2 + self.thickness - self.length / 2
        z_center = (self.model.usbc.height - self.model.pcb_height) / 2

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

        y_start = self.model.pcb_width / 2
        z_start = -self.model.pcb_height / 2

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
                z_start + self.adapter_height / 2,
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

        height = self.adapter_height + 5.0
        x_pos = self.model.mounting_hole_x
        y_pos = self.model.mounting_hole_y

        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            circular_segments=60,
            center=True,
        )
        z_center = (self.model.usbc.height - self.model.pcb_height) / 2
        return (
            hole.translate([x_pos, y_pos, 0])
            + hole.translate([-x_pos, y_pos, 0])
        ).translate([0, 0, z_center])

    def assemble(self) -> manifold3d.Manifold:

        return (self.body - self.screw_holes).translate(self.model.body_offset)


if __name__ == "__main__":
    adapter = injector.get(USBCAdapterCAD)
    adapter.program(sys.argv)
