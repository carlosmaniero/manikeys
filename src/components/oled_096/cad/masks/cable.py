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
class Oled096PlacementCableMaskCAD(ManifoldObject):
    model: Oled096PlacementModel

    def assemble(self) -> manifold3d.Manifold:
        extra_thickness = self.model.thickness
        r = self.model.cable_mask_size[1] / 2 + extra_thickness
        w = self.model.cable_mask_size[0]
        z_height = self.model.cable_mask_size[2]

        cyl = manifold3d.Manifold.cylinder(
            z_height, r, circular_segments=32, center=True
        )
        left_cyl = cyl.translate([-w / 2, 0, 0])
        right_cyl = cyl.translate([w / 2, 0, 0])
        rounded_rect = manifold3d.Manifold.batch_hull([left_cyl, right_cyl])

        return rounded_rect.translate(self.model.cable_mask_coords)


if __name__ == "__main__":
    mask = injector.get(Oled096PlacementCableMaskCAD)
    mask.program(sys.argv)
