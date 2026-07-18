from __future__ import annotations
from globals.wall.parameters import WallParameters
from structure.body.parameters import BodyParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from switches.socket.mount.models import MountCavityModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountShellCAD(ManifoldObject):
    model: MountCavityModel
    body: BodyModel
    wall_parameters: WallParameters
    body_parameters: BodyParameters

    def assemble(self) -> manifold3d.Manifold:
        divider_size = (
            self.wall_parameters.thickness * 2
            + self.body_parameters.clearance * 2
        )
        divider_y = self.model.divider_y - divider_size / 2

        body_divider = manifold3d.Manifold.cube(
            [
                self.model.width * 3,
                divider_size,
                self.model.height * 2,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x() - self.model.width,
                divider_y,
                self.model.bottom_z,
            ]
        )

        side_divider_size = self.body_parameters.clearance

        side_divider = manifold3d.Manifold.cube(
            [
                side_divider_size,
                self.body.divider_y - self.body.start_y(),
                self.body.height * 2,
            ],
            center=False,
        ).translate(
            [
                self.body.hand_support_end_x + self.wall_parameters.thickness,
                self.body.start_y(),
                self.body.bottom_z,
            ]
        )

        screw_walls = load_stl_to_manifold(
            "build/switches/socket/mount/cad/screw_clearance_cavity.stl"
        ) ^ load_stl_to_manifold("build/switches/socket/mount/cad/body.stl")

        return (
            load_stl_to_manifold("build/switches/socket/mount/cad/body.stl")
            - load_stl_to_manifold(
                "build/switches/socket/mount/cad/cavity_sections.stl"
            )
            - load_stl_to_manifold(
                "build/connectors/rj45/cad/masks/placement.stl"
            )
            - load_stl_to_manifold(
                "build/connectors/usbc/cad/masks/placement.stl"
            )
            + screw_walls
            - load_stl_to_manifold(
                "build/switches/socket/mount/cad/screw_clearance.stl"
            )
            + load_stl_to_manifold(
                "build/switches/cad/switch_hole_decorator_shell_grid.stl"
            )
            - load_stl_to_manifold("build/switches/cad/switch_hole_grid.stl")
            - load_stl_to_manifold("build/switches/cad/switch_thumb_hole.stl")
            - load_stl_to_manifold("build/connectors/pogo/cad/cable_path.stl")
            - load_stl_to_manifold(
                "build/components/light_indicator/cad/masks/body_shell.stl"
            )
            - load_stl_to_manifold(
                "build/components/oled_096/cad/masks/shell.stl"
            )
            - side_divider
            - body_divider
        )


if __name__ == "__main__":
    shell = injector.get(MountShellCAD)
    shell.program(sys.argv)
