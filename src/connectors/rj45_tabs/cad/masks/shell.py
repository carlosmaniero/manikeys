from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from connectors.rj45_tabs.model import AdapterPlacementModel


@singleton
@inject
@dataclass
class AdapterShellMaskCAD(ManifoldObject):
    model: AdapterPlacementModel

    def assemble(self) -> manifold3d.Manifold:
        mask = manifold3d.Manifold.cube(
            self.model.adapter_model.mask_shell_size, center=True
        )
        return (
            mask.rotate([0, 180, 0])
            .rotate([90, 0, -90])
            .translate(self.model.translation_coords)
        )


if __name__ == "__main__":
    mask_cad = injector.get(AdapterShellMaskCAD)
    mask_cad.program(sys.argv)
