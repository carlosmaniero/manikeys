from __future__ import annotations
import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from models.components.oled_096 import Oled096Model


@singleton
@inject
@dataclass
class Oled096LidCAD(ManifoldObject):
    model: Oled096Model

    @property
    def body(self) -> M:
        return M.cube(
            [
                self.model.body[0],
                self.model.parameters.panel[1],
                self.model.thickness,
            ],
            center=True,
        )

    @property
    def screw_holes(self) -> M:
        holes = M()
        for hole in self.model.screw_holes:
            holes += M.cylinder(
                self.model.thickness + 1,
                self.model.global_parameters.screw.m2_diameter / 2,
                circular_segments=32,
                center=True,
            ).translate([hole[0], hole[1], 0.0])

        return holes.translate(self.model.screw_holes_translation)

    def assemble(self) -> M:
        return self.body - self.screw_holes


if __name__ == "__main__":
    lid = injector.get(Oled096LidCAD)
    lid.program(sys.argv)
