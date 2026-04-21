from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.usbc import USBCModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCMaskCAD(ManifoldObject):
    model: USBCModel

    def assemble(self) -> manifold3d.Manifold:
        # Now it only returns the connector mask hole at the correct world position
        return load_stl_to_manifold(
            "build/cad/connectors/usbc_connector_mask.stl"
        ).translate(self.model.body_offset)


if __name__ == "__main__":
    mask = injector.get(USBCMaskCAD)
    mask.program(sys.argv)
