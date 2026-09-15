from __future__ import annotations
import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import SwitchHoleDecoratorShellModel
from core.manifold_ext.helpers import half_rounded
from core.manifold_ext.object import ManifoldObject
from core.context import injector


@singleton
@inject
@dataclass
class SwitchHoleDecoratorCableMatrixCAD(ManifoldObject):
    model: SwitchHoleDecoratorShellModel

    @property
    def y_cable_path(self) -> manifold3d.Manifold:
        body = half_rounded(
            self.model.y_cable_path_cube_size,
            circular_segments=8,
        ).rotate([180, 0, 0])
        return body.translate(self.model.y_cable_path_translation)

    @property
    def x_cable_path(self) -> manifold3d.Manifold:
        body = (
            half_rounded(
                self.model.x_cable_path_cube_size,
                circular_segments=8,
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
            circular_segments=8,
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
            circular_segments=8,
        )
        return hole.rotate([0, 90, 0]).translate(
            self.model.x_cable_hole_translation
        )

    @property
    def block(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            self.model.block_size, center=True
        ).translate(self.model.block_translation)

    def assemble(self) -> manifold3d.Manifold:
        return (
            manifold3d.Manifold.hull(self.y_cable_path + self.x_cable_path)
            + self.block
            - self.cable_hole
            - self.x_cable_hole
        )


if __name__ == "__main__":
    switch_hole_decorator_cable_matrix = injector.get(
        SwitchHoleDecoratorCableMatrixCAD
    )
    switch_hole_decorator_cable_matrix.program(sys.argv)
