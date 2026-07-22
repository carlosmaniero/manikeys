from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from components.cable_hook.model import CableHookModel


@singleton
@inject
@dataclass
class CableHookCAD(ManifoldObject):
    model: CableHookModel

    def assemble(self) -> manifold3d.Manifold:
        inner_radius = self.model.cable_radius
        radius = self.model.outer_radius
        offset_x = self.model.offset_x
        height = self.model.parameters.height

        outer_cyl = manifold3d.Manifold.cylinder(
            height=height,
            radius_low=radius,
            circular_segments=16,
        )

        outer_cube = manifold3d.Manifold.cube(
            [offset_x, radius * 2, height],
            center=True,
        ).translate([offset_x / 2, 0, height / 2])

        outer = outer_cyl + outer_cube

        inner_cyl = manifold3d.Manifold.cylinder(
            height=height,
            radius_low=inner_radius,
            circular_segments=16,
        )

        inner_cube = manifold3d.Manifold.cube(
            [offset_x + 0.2, inner_radius * 2, height + 0.2],
            center=True,
        ).translate([offset_x / 2 + 0.1, 0, height / 2])

        inner = inner_cyl + inner_cube

        return outer - inner


if __name__ == "__main__":
    cable_hook = injector.get(CableHookCAD)
    cable_hook.program(sys.argv)
