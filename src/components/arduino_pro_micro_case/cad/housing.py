from __future__ import annotations
import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from components.arduino_pro_micro_case.model import ArduinoProMicroCaseModel


@singleton
@inject
@dataclass
class ArduinoProMicroCaseCAD(ManifoldObject):
    model: ArduinoProMicroCaseModel

    @property
    def pcb_placement(self) -> M:
        return M.cube(
            self.model.pcb_placement_dimensions, center=True
        ).translate(self.model.pcb_placement_coords)

    @property
    def screw_holes(self) -> M:
        holes = M()
        height = self.model.dimensions[2] + 2.0
        radius = self.model.screw_hole_radius
        for coords in self.model.screw_holes_coords:
            holes += M.cylinder(
                height, radius, circular_segments=32, center=True
            ).translate(coords)
        return holes

    @property
    def pins_clearance(self) -> M:
        cutouts = M()
        radius = self.model.pins_clearance_radius
        height = self.model.pins_clearance_dimensions[2] + 2.0
        y_offset = self.model.pins_clearance_y_offset

        cyl = M.cylinder(height, radius, center=True, circular_segments=32)
        pill = (
            cyl.translate([0, y_offset, 0]) + cyl.translate([0, -y_offset, 0])
        ).hull()

        for coords in self.model.pins_clearance_coords:
            cutouts += pill.translate(coords)
        return cutouts

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

    def assemble(self) -> M:
        return (
            self.body
            - self.pcb_placement
            - self.screw_holes
            - self.pins_clearance
        )


if __name__ == "__main__":
    box = injector.get(ArduinoProMicroCaseCAD)
    box.program(sys.argv)
