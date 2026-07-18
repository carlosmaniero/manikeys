from __future__ import annotations
from globals.wall.parameters import WallParameters
from structure.body.parameters import BodyParameters
from core.context import injector
import sys
import manifold3d
from dataclasses import dataclass
from switches.socket.mount.models import MountCavityModel
from injector import inject, singleton
from core.loader import load_stl_to_manifold
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountCavitySectionsCAD(ManifoldObject):
    model: MountCavityModel
    wall_parameters: WallParameters
    body_parameters: BodyParameters

    def assemble(self) -> manifold3d.Manifold:
        divider_size = (
            self.wall_parameters.thickness * 4
            + self.body_parameters.clearance * 2
        )
        divider_y = self.model.divider_y - divider_size / 2

        divider = manifold3d.Manifold.cube(
            [
                self.model.width,
                divider_size,
                self.model.height * 2,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                divider_y,
                self.model.bottom_z,
            ]
        )

        side_section = manifold3d.Manifold.cube(
            [
                self.model.hand_support_end_x - self.model.hand_support_start_x,
                divider_y - self.model.start_y(),
                self.model.height * 2,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                self.model.start_y(),
                self.model.bottom_z,
            ]
        )

        body = load_stl_to_manifold(
            "build/switches/socket/mount/cad/cavity.stl"
        )

        return body - (divider + side_section)


if __name__ == "__main__":
    cavity_sections = injector.get(MountCavitySectionsCAD)
    cavity_sections.program(sys.argv)
