from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from models.components.light_indicator.led import Led
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class LedCad(ManifoldObject):
    model: Led

    @property
    def pcb(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cylinder(
            height=self.model.pcb_height,
            radius_low=self.model.pcb_radius,
            radius_high=self.model.pcb_radius,
            center=True,
            circular_segments=32,
        )

    @property
    def led(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [self.model.led_size, self.model.led_size, self.model.led_height],
            center=True,
        ).translate([0, 0, self.model.led_height])

    def assemble(self) -> manifold3d.Manifold:
        return self.pcb + self.led


if __name__ == "__main__":
    adapter = injector.get(LedCad)
    adapter.program(sys.argv)
