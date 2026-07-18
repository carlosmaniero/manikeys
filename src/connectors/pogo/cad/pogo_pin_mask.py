from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.helpers import capsule
from connectors.pogo.models import PogoPinModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class PogoPinMaskCAD(ManifoldObject):
    model: PogoPinModel

    @property
    def body_mask(self) -> manifold3d.Manifold:
        # Main body with some error margin
        error = 0.2
        return capsule(
            [
                self.model.body_length + error * 2,
                self.model.body_width + error * 2,
                self.model.body_height + error,
            ],
            circular_segments=60,
        ).translate([0, 0, error / 2])

    @property
    def flange_mask(self) -> manifold3d.Manifold:
        error = 0.2
        return capsule(
            [
                self.model.flange_full_length + error * 2,
                self.model.body_width + error * 2,
                self.model.flange_thickness + error,
            ],
            circular_segments=60,
        ).translate(
            [
                0,
                0,
                self.model.flange_z_offset,
            ]
        )

    @property
    def pin_holes(self) -> manifold3d.Manifold:
        # Holes for pins to pass through the adapter face
        radius = self.model.pin_tip_diameter / 2 + 0.3
        height = 10.0  # Tall enough to pass through
        pitch = self.model.pin_pitch
        count = self.model.pin_count

        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            circular_segments=30,
            center=True,
        ).translate([0, 0, height / 2 - self.model.body_height / 2])

        start_x = self.model.pins_start_x
        holes = hole.translate([start_x, 0, 0])
        for i in range(1, count):
            holes += hole.translate([start_x + i * pitch, 0, 0])

        return holes

    def assemble(self) -> manifold3d.Manifold:
        return self.body_mask + self.flange_mask + self.pin_holes


if __name__ == "__main__":
    mask = injector.get(PogoPinMaskCAD)
    mask.program(sys.argv)
