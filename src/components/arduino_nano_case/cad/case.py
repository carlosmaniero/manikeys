from __future__ import annotations
import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from components.arduino_nano_case.model import ArduinoNanoCaseModel


@singleton
@inject
@dataclass
class ArduinoNanoCaseCAD(ManifoldObject):
    model: ArduinoNanoCaseModel

    @property
    def body(self) -> M:
        r = self.model.body_fillet_radius
        w, d, h = self.model.dimensions

        cyl = M.cylinder(h, r, center=True, circular_segments=32)

        x_off = w / 2 - r
        y_off = d / 2 - r

        c1 = cyl.translate([x_off, y_off, 0])
        c2 = cyl.translate([-x_off, y_off, 0])
        c3 = cyl.translate([x_off, -y_off, 0])
        c4 = cyl.translate([-x_off, -y_off, 0])

        return (c1 + c2 + c3 + c4).hull()

    @property
    def towers(self) -> M:
        towers = M()
        height = self.model.tower_height
        radius = self.model.tower_radius

        cyl = M.cylinder(height, radius, center=True, circular_segments=32)
        for coords in self.model.tower_coords:
            towers += cyl.translate(coords)

        return towers

    @property
    def screw_holes(self) -> M:
        holes = M()
        height = self.model.screw_holes_height
        radius = self.model.screw_hole_radius

        cyl = M.cylinder(height, radius, center=True, circular_segments=32)
        for coords in self.model.screw_holes_coords:
            holes += cyl.translate(coords)
        return holes

    def assemble(self) -> M:
        return (self.body + self.towers) - self.screw_holes


if __name__ == "__main__":
    box = injector.get(ArduinoNanoCaseCAD)
    box.program(sys.argv)
