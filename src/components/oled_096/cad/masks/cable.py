from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.helpers import capsule
from components.oled_096.model import Oled096PlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class Oled096PlacementCableMaskCAD(ManifoldObject):
    model: Oled096PlacementModel

    def assemble(self) -> manifold3d.Manifold:
        extra_thickness = self.model.thickness
        r = self.model.cable_mask_size[1] / 2 + extra_thickness
        w = self.model.cable_mask_size[0]
        z_height = self.model.cable_mask_size[2]

        rounded_rect = capsule(
            [w + 2 * r, 2 * r, z_height], circular_segments=32
        )

        return rounded_rect.translate(self.model.cable_mask_coords)


if __name__ == "__main__":
    mask = injector.get(Oled096PlacementCableMaskCAD)
    mask.program(sys.argv)
