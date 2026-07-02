from __future__ import annotations
from globals.wall.parameters import WallParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from connectors.usbc.model import USBCModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCPlacementMaskCAD(ManifoldObject):
    wall_parameters: WallParameters
    model: USBCModel
    body_model: BodyModel

    @property
    def thickness(self) -> float:
        return self.wall_parameters.thickness

    @property
    def width(self) -> float:
        return (
            self.model.pcb_length
            + self.thickness * 6
            + self.wall_parameters.fillet
        )

    @property
    def length(self) -> float:
        adapter_base_length = (
            self.thickness + self.model.mounting_hole_diameter + self.thickness
        )
        return adapter_base_length + self.thickness * 8

    @property
    def mask_height(self) -> float:
        return (
            self.thickness
            + self.model.pcb_height
            + self.model.usbc.height
            + self.thickness
        )

    @property
    def main_block(self) -> manifold3d.Manifold:
        # Align with the adapter's footprint but larger
        # Wall is at +Y (pcb_width/2)

        adapter_base_length = (
            self.thickness + self.model.mounting_hole_diameter + self.thickness
        )
        adapter_y_center = (
            self.model.pcb_width / 2 + self.thickness - adapter_base_length / 2
        )
        # y_center relative to adapter center
        y_center = adapter_y_center - self.thickness

        z_center = (
            self.model.pcb_height / 2
            + self.thickness
            - (self.thickness + self.model.pcb_height + self.model.usbc.height)
            / 2
        )

        return manifold3d.Manifold.cube(
            [
                self.width,
                self.length,
                self.mask_height + self.body_model.highest,
            ],
            center=True,
        ).translate(
            [
                0,
                y_center,
                z_center + self.body_model.highest / 2,
            ]
        )

    def assemble(self) -> manifold3d.Manifold:
        offset = self.model.body_offset
        return self.main_block.translate(
            [
                self.body_model.start_x() + self.width / 2,
                offset[1],
                offset[2],
            ]
        )


if __name__ == "__main__":
    mask = injector.get(USBCPlacementMaskCAD)
    mask.program(sys.argv)
