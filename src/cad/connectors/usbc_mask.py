from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.usbc import USBCModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCMaskCAD(ManifoldObject):
    model: USBCModel

    @property
    def thickness(self) -> float:
        return self.model.parameters.body.thickness

    @property
    def width(self) -> float:
        return self.model.pcb_width + self.thickness * 2

    @property
    def length(self) -> float:
        return self.model.pcb_length + self.thickness * 2

    @property
    def adapter_height(self) -> float:
        return self.model.usbc.height + self.thickness * 2

    @property
    def main_block(self) -> manifold3d.Manifold:
        # Simplified block for the mask, matches the adapter's outer bounds
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
                0,
                (self.model.usbc.height - self.model.pcb_height) / 2,
            ]
        )

    def assemble(self) -> manifold3d.Manifold:
        return self.main_block.translate(self.model.body_offset)


if __name__ == "__main__":
    mask = injector.get(USBCMaskCAD)
    mask.program(sys.argv)
