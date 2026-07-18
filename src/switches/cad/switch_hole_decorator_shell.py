from __future__ import annotations
import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import SwitchHoleDecoratorShellModel
from globals.wall.parameters import WallParameters
from core.manifold_ext.helpers import rounded_box, half_rounded
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class SwitchHoleDecoratorShellCAD(ManifoldObject):
    model: SwitchHoleDecoratorShellModel
    wall_parameters: WallParameters

    @property
    def y_cable_path(self) -> manifold3d.Manifold:
        body = half_rounded(
            self.model.y_cable_path_cube_size,
        ).rotate([180, 0, 0])
        return body.translate(self.model.y_cable_path_translation)

    @property
    def x_cable_path(self) -> manifold3d.Manifold:
        body = (
            half_rounded(
                self.model.x_cable_path_cube_size,
            )
            .rotate([0, 0, 90])
            .rotate([180, 0, 0])
        )
        return body.translate(self.model.x_cable_path_translation)

    @property
    def cable_hole(self) -> manifold3d.Manifold:
        hole = manifold3d.Manifold.cylinder(
            self.model.cable_hole_length,
            self.model.cable_hole_radius,
            center=True,
            circular_segments=32,
        )
        return hole.rotate([90, 0, 0]).translate(
            self.model.y_cable_path_translation
        )

    @property
    def x_cable_hole(self) -> manifold3d.Manifold:
        hole = manifold3d.Manifold.cylinder(
            self.model.x_cable_hole_length,
            self.model.cable_hole_radius,
            center=True,
            circular_segments=32,
        )
        return hole.rotate([0, 90, 0]).translate(
            self.model.x_cable_hole_translation
        )

    @property
    def body(self) -> manifold3d.Manifold:
        return rounded_box(
            self.model.cube_size, self.wall_parameters.thickness
        ).translate(self.model.translation)

    @property
    def hot_swap_placement_mask(self) -> manifold3d.Manifold:
        return (
            load_stl_to_manifold(
                "build/switches/socket/cad/hot_swap_placement_mask.stl"
            )
            .rotate([180, 0, 180])
            .translate(self.model.mask_translation)
        )

    @property
    def switch_hole(self) -> manifold3d.Manifold:
        return load_stl_to_manifold("build/switches/cad/switch_hole.stl")

    def assemble(self) -> manifold3d.Manifold:
        return (
            self.body
            - self.hot_swap_placement_mask
            - self.switch_hole
            + manifold3d.Manifold.hull(self.y_cable_path + self.x_cable_path)
            - self.cable_hole
            - self.x_cable_hole
        )


if __name__ == "__main__":
    switch_hole_decorator_shell = injector.get(SwitchHoleDecoratorShellCAD)
    switch_hole_decorator_shell.program(sys.argv)
