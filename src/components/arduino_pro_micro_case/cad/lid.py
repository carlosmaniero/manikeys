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
class ArduinoProMicroCaseLidCAD(ManifoldObject):
    model: ArduinoProMicroCaseModel

    @property
    def pcb_placement(self) -> M:
        return M.cube(
            self.model.pcb_placement_dimensions, center=True
        ).translate(self.model.pcb_placement_coords)

    @property
    def usb_c_cutout(self) -> M:
        radius = self.model.usb_c_cylinder_radius
        height = self.model.usb_c_cylinder_height
        offset = self.model.usb_c_cylinder_offset

        cyl = M.cylinder(
            height, radius, center=True, circular_segments=32
        ).rotate([90, 0, 0])

        left = cyl.translate([-offset, 0, 0])
        right = cyl.translate([offset, 0, 0])

        return (left + right).hull().translate(self.model.usb_c_cutout_coords)

    @property
    def pins_clearance(self) -> M:
        cutouts = M()
        radius = self.model.pins_clearance_radius
        height = self.model.lid_dimensions[2] + 2.0
        y_offset = self.model.pins_clearance_y_offset

        cyl = M.cylinder(height, radius, center=True, circular_segments=32)
        pill = (
            # Extend far into positive Y to cut through the back wall
            cyl.translate([0, 50, 0]) + cyl.translate([0, -y_offset, 0])
        ).hull()

        for coords in self.model.pins_clearance_coords:
            c = coords.copy()
            c[2] = self.model.lid_coords[2]
            cutouts += pill.translate(c)
        return cutouts

    @property
    def screw_holes(self) -> M:
        holes = M()
        height = self.model.lid_dimensions[2]
        radius = self.model.screw_hole_radius
        for coords in self.model.screw_holes_coords:
            c = coords.copy()
            c[2] = self.model.lid_coords[2]
            holes += M.cylinder(
                height, radius, circular_segments=32, center=True
            ).translate(c)
        return holes

    @property
    def screw_heads(self) -> M:
        heads = M()
        radius = self.model.screw_head_radius
        height = self.model.screw_head_height

        lid_top = self.model.lid_coords[2] + self.model.lid_thickness / 2
        bottom_of_head = lid_top - self.model.screw_head_height
        z_center = bottom_of_head + height / 2

        for coords in self.model.screw_holes_coords:
            c = coords.copy()
            c[2] = z_center
            heads += M.cylinder(
                height, radius, circular_segments=32, center=True
            ).translate(c)
        return heads

    @property
    def body(self) -> M:
        r = self.model.body_fillet_radius
        w, d, h = self.model.lid_dimensions

        cyl = M.cylinder(h, r, center=True, circular_segments=32)

        x_off = w / 2 - r
        y_off = d / 2 - r

        c1 = cyl.translate([x_off, y_off, 0])
        c2 = cyl.translate([-x_off, y_off, 0])
        c3 = cyl.translate([x_off, -y_off, 0])
        c4 = cyl.translate([-x_off, -y_off, 0])

        return (c1 + c2 + c3 + c4).hull().translate(self.model.lid_coords)

    def assemble(self) -> M:
        return (
            self.body
            - self.pcb_placement
            - self.usb_c_cutout
            - self.pins_clearance
            - self.screw_holes
            - self.screw_heads
        )


if __name__ == "__main__":
    box = injector.get(ArduinoProMicroCaseLidCAD)
    box.program(sys.argv)
