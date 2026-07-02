from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from connectors.usbc.model import USBCModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCMaskCAD(ManifoldObject):
    model: USBCModel
    body_model: BodyModel

    @property
    def main_block(self) -> manifold3d.Manifold:
        y_center = (
            self.model.pcb_width / 2
            + self.model.thickness
            - self.model.length / 2
        )
        z_center = (
            self.model.pcb_height / 2
            + self.model.thickness
            - self.model.adapter_height / 2
        )

        return manifold3d.Manifold.cube(
            [
                self.model.width,
                self.model.length,
                self.model.adapter_height + self.body_model.highest,
            ],
            center=True,
        ).translate(
            [
                0,
                y_center,
                z_center + self.body_model.highest / 2,
            ]
        )

    @property
    def body(self) -> manifold3d.Manifold:
        return load_stl_to_manifold(
            "build/connectors/usbc/cad/masks/connector.stl"
        )

    def assemble(self) -> manifold3d.Manifold:
        return self.main_block.translate(self.model.body_offset)


if __name__ == "__main__":
    mask = injector.get(USBCMaskCAD)
    mask.program(sys.argv)
