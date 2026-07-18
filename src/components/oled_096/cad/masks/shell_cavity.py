from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from components.oled_096.model import Oled096PlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class Oled096PlacementShellCavityMaskCAD(ManifoldObject):
    model: Oled096PlacementModel

    def assemble(self) -> manifold3d.Manifold:
        extra_thickness = self.model.thickness / 2
        size = [
            self.model.shell_mask_size[0],
            self.model.shell_mask_size[1] + 2 * extra_thickness,
            self.model.shell_mask_size[2]
            + 2 * extra_thickness
            - self.model.thickness / 2,
        ]
        return manifold3d.Manifold.cube(
            size,
            center=True,
        ).translate(self.model.shell_mask_coords)


if __name__ == "__main__":
    mask = injector.get(Oled096PlacementShellCavityMaskCAD)
    mask.program(sys.argv)
