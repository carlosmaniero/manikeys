from __future__ import annotations
from globals.wall.parameters import WallParameters
from globals.screw.parameters import ScrewParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from connectors.rj11.model import RJ11Model
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ11AdapterPlacementCAD(ManifoldObject):
    wall_parameters: WallParameters
    screw_parameters: ScrewParameters
    model: RJ11Model
    body_model: BodyModel

    @property
    def height(self) -> float:
        return (
            self.model.rj11.socket_height
            - self.model.rj11.bottom_notch_height
            - self.model.rj11.adapter_head_height
        )

    @property
    def width(self) -> float:
        return self.model.rj11.width + self.wall_parameters.thickness * 2

    @property
    def tab_width(self) -> float:
        return (
            self.screw_parameters.m2_diameter
            + self.wall_parameters.thickness * 2
        )

    @property
    def tab_length(self) -> float:
        return self.wall_parameters.thickness * 3

    @property
    def tabs(self) -> manifold3d.Manifold:
        tab = manifold3d.Manifold.cube(
            [self.tab_width, self.tab_length, self.model.rj11.height],
            center=True,
        )

        x_pos = self.width / 2 + self.tab_width / 2
        y_front = self.model.rj11.length / 2 + self.model.rj11.error_margin * 3
        # Face-to-face with adapter tab:
        # Adapter tab is at y_front - 3*t (center), range [y_front - 3.5*t, y_front - 2.5*t]
        # Placement is 3*t long. If it touches y_front - 2.5*t and extends forward:
        # Range [y_front - 2.5*t, y_front + 0.5*t]. Center: y_front - 1.0*t
        y_pos = y_front - self.wall_parameters.thickness * 1.0

        return tab.translate([x_pos, y_pos, 0]) + tab.translate(
            [-x_pos, y_pos, 0]
        )

    @property
    def screw_holes(self) -> manifold3d.Manifold:
        radius = self.screw_parameters.m2_diameter / 2
        # Hole must align with adapter hole at y_front - 3*t
        height = self.tab_length * 2  # Long enough to pass through everything

        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            center=True,
            circular_segments=60,
        ).rotate([90, 0, 0])

        x_pos = self.width / 2 + self.tab_width / 2
        y_front = self.model.rj11.length / 2 + self.model.rj11.error_margin * 3
        # Align with adapter screw hole
        y_pos = y_front - self.wall_parameters.thickness * 3

        return hole.translate([x_pos, y_pos, 0]) + hole.translate(
            [-x_pos, y_pos, 0]
        )

    def assemble(self) -> manifold3d.Manifold:
        max_x = self.width / 2 + self.tab_width
        max_y = self.model.rj11.length / 2 + self.wall_parameters.thickness
        placement = (self.tabs - self.screw_holes).translate(
            [
                self.body_model.end_x() - self.wall_parameters.fillet - max_x,
                self.body_model.end_y()
                - max_y
                + self.wall_parameters.thickness
                - self.model.rj11.error_margin * 2,
                self.body_model.bottom_z
                + self.wall_parameters.thickness
                + self.model.rj11.height / 2
                + self.height,
            ]
        )

        body = load_stl_to_manifold("build/structure/body/shape.stl")
        return placement ^ body


if __name__ == "__main__":
    placement = injector.get(RJ11AdapterPlacementCAD)
    placement.program(sys.argv)
