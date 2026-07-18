from __future__ import annotations
from globals.wall.parameters import WallParameters
from structure.body.parameters import BodyParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_many_stl_to_manifold
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

        paths = [
            "build/switches/socket/mount/cad/body.stl",
            "build/switches/socket/mount/cad/screw_clearance_cavity.stl",
            "build/switches/socket/mount/cad/cavity_sections.stl",
            "build/connectors/rj45/cad/masks/placement.stl",
            "build/connectors/usbc/cad/masks/placement.stl",
            "build/switches/socket/mount/cad/screw_clearance.stl",
            "build/switches/cad/switch_hole_decorator_shell_grid.stl",
            "build/switches/cad/switch_hole_grid.stl",
            "build/switches/cad/switch_thumb_hole.stl",
            "build/connectors/pogo/cad/cable_path.stl",
            "build/components/light_indicator/cad/masks/body_shell.stl",
            "build/components/oled_096/cad/masks/shell.stl",
            "build/components/oled_096/cad/masks/shell_cavity.stl",
            "build/components/oled_096/cad/masks/cable.stl",
        ]

        (
            body,
            screw_clearance_cavity,
            cavity_sections,
            rj45_placement,
            usbc_placement,
            screw_clearance,
            switch_hole_decorator_shell_grid,
            switch_hole_grid,
            switch_thumb_hole,
            cable_path,
            light_indicator_body_shell,
            oled_shell,
            oled_shell_cavity,
            oled_cable,
        ) = load_many_stl_to_manifold(paths)

        screw_walls = screw_clearance_cavity ^ body
        oled_walls = oled_shell_cavity ^ body

        return (
            body
            - cavity_sections
            - rj45_placement
            - usbc_placement
            + oled_walls
            + screw_walls
            - screw_clearance
            + switch_hole_decorator_shell_grid
            - switch_hole_grid
            - switch_thumb_hole
            - cable_path
            - light_indicator_body_shell
            - side_divider
            - body_divider
            - oled_shell
            - oled_cable
        )


if __name__ == "__main__":
    shell = injector.get(MountShellCAD)
    shell.program(sys.argv)
