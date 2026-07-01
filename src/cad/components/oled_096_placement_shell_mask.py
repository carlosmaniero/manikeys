from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from models.components.oled_096 import Oled096PlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class Oled096PlacementShellMaskCAD(ManifoldObject):
    model: Oled096PlacementModel

    def assemble(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            self.model.shell_mask_size,
            center=True,
        ).translate(self.model.shell_mask_coords)


if __name__ == "__main__":
    mask = injector.get(Oled096PlacementShellMaskCAD)
    mask.program(sys.argv)
