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
class Oled096CAD(ManifoldObject):
    model: Oled096Model

    @property
    def pcb_pocket(self) -> M:
        return M.cube(self.model.pcb_pocket, center=True).translate(
            self.model.pcb_pocket_coords
        )

    @property
    def panel_pocket(self) -> M:
        return M.cube(self.model.panel_pocket, center=True).translate(
            self.model.panel_pocket_coords
        )

    @property
    def body(self) -> M:
        return M.cube(self.model.body, center=True)

    @property
    def screw_holes(self) -> M:
        holes = M()
        for hole in self.model.screw_holes:
            holes += M.cylinder(
                self.model.parameters.screw_hole_depth,
                self.model.parameters.screw_hole_radius,
                circular_segments=32,
                center=True,
            ).translate(hole)

        return holes.translate(self.model.screw_holes_translation)

    @property
    def flat_cable_clearance(self) -> M:
        clearance = self.model.parameters.flat_cable_clearance
        height = self.model.pcb_pocket[1] / 2 - self.model.panel_pocket[1] / 2
        return M.cube(
            [
                self.model.parameters.flat_cable_width,
                height,
                clearance,
            ],
            center=True,
        ).translate(
            [
                0,
                -height / 2 - self.model.panel_pocket[1] / 2,
                clearance / 2
                + self.model.body[2] / 2
                - self.model.parameters.display_height,
            ]
        )

    @property
    def cable_clearance(self) -> M:
        return M.cube(self.model.cable_clearance, center=True).translate(
            self.model.cable_clearance_coords
        )

    @property
    def lid_pocket(self) -> M:
        return M.cube(self.model.lid_pocket, center=True).translate(
            self.model.lid_pocket_coords
        )

    def assemble(self) -> M:
        return (
            self.body
            - self.pcb_pocket
            - self.panel_pocket
            - self.flat_cable_clearance
            - self.cable_clearance
            - self.lid_pocket
            - self.screw_holes
        )


if __name__ == "__main__":
    oled = injector.get(Oled096CAD)
    oled.program(sys.argv)
