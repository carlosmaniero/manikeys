from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from models.parameters import Parameters
from switches.socket.mount.models import MountCavityModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MountShellCAD(ManifoldObject):
    model: MountCavityModel
    body: BodyModel
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        divider_size = (
            self.parameters.wall.thickness * 2
            + self.parameters.body.clearance * 2
        )
        divider_y = self.model.divider_y - divider_size / 2

        body_divider = manifold3d.Manifold.cube(
            [
                self.model.width * 3,
                divider_size,
                self.model.sphere.highest + self.parameters.body.height,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x() - self.model.width,
                divider_y,
                -self.parameters.body.height,
            ]
        )

        height = self.model.sphere.highest + self.parameters.body.height

        side_divider_size = self.parameters.body.clearance

        side_divider = manifold3d.Manifold.cube(
            [
                side_divider_size,
                self.body.divider_y - self.body.start_y(),
                height * 2,
            ],
            center=False,
        ).translate(
            [
                self.body.hand_support_end_x + self.parameters.wall.thickness,
                self.body.start_y(),
                -self.parameters.body.height,
            ]
        )

        return (
            load_stl_to_manifold("build/cad/socket_placement.stl")
            - load_stl_to_manifold(
                "build/cad/socket_placement_inner_sections.stl"
            )
            - side_divider
            - body_divider
            - load_stl_to_manifold("build/cad/connectors/placement_mask.stl")
            - load_stl_to_manifold(
                "build/cad/connectors/usbc_placement_mask.stl"
            )
            - load_stl_to_manifold("build/cad/body_screw_mask.stl")
            - load_stl_to_manifold("build/switches/cad/switch_hole_grid.stl")
            - load_stl_to_manifold("build/switches/cad/switch_thumb_hole.stl")
            - load_stl_to_manifold("build/cad/cable_path.stl")
            - load_stl_to_manifold(
                "build/cad/components/light_indicator/body_shell_mask.stl"
            )
            - load_stl_to_manifold(
                "build/cad/components/oled_096_placement_shell_mask.stl"
            )
        )


if __name__ == "__main__":
    shell = injector.get(MountShellCAD)
    shell.program(sys.argv)
