from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from globals.wall.parameters import WallParameters
from switches.socket.mount.models import ColCablePathModel


@singleton
@inject
@dataclass
class ColCablePathCAD(ManifoldObject):
    model: ColCablePathModel
    wall_parameters: WallParameters

    def assemble(self) -> manifold3d.Manifold:
        inner_radius = self.model.cable_radius
        radius = self.model.outer_radius
        offset_x = self.wall_parameters.thickness
        result = manifold3d.Manifold()

        for x, y, z_min, height in self.model.path:
            outer_cyl = manifold3d.Manifold.cylinder(
                height=height,
                radius_low=radius,
                circular_segments=16,
            ).translate([x, y, z_min])

            outer_cube = manifold3d.Manifold.cube(
                [offset_x, radius * 2, height],
                center=True,
            ).translate([x + offset_x / 2, y, z_min + height / 2])

            outer = outer_cyl + outer_cube

            inner_cyl = manifold3d.Manifold.cylinder(
                height=height,
                radius_low=inner_radius,
                circular_segments=16,
            ).translate([x, y, z_min])

            inner_cube = manifold3d.Manifold.cube(
                [offset_x + 0.2, inner_radius * 2, height + 0.2],
                center=True,
            ).translate([x + offset_x / 2 + 0.1, y, z_min + height / 2])

            inner = inner_cyl + inner_cube

            result += outer - inner

        return result


if __name__ == "__main__":
    cable_path = injector.get(ColCablePathCAD)
    cable_path.program(sys.argv)
