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
class USBCPlacementMaskCAD(ManifoldObject):
    parameters: Parameters
    model: USBCModel
    body_model: BodyModel

    @property
    def thickness(self) -> float:
        return self.parameters.body.thickness

    @property
    def width(self) -> float:
        # Long side is X. Extend to reach start_x and add extra clearance on the other side.
        return (
            self.model.pcb_length
            + self.thickness * 6
            + self.parameters.body.fillet
        )

    @property
    def length(self) -> float:
        adapter_base_length = (
            self.thickness + self.model.mounting_hole_diameter + self.thickness
        )
        return adapter_base_length + self.thickness

    @property
    def mask_height(self) -> float:
        # Cover the whole height of the adapter and then some
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
        # Translate so that the left face is at start_x
        # And the Y/Z match the adapter's body_offset
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
