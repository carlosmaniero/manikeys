from __future__ import annotations
import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from core.manifold_ext.helpers import rounded_box
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
        return rounded_box(self.model.dimensions, r, circular_segments=32)

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
