from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from structure.body.parameters import BodyParameters
from switches.model import Layout
from switches.socket.mount.models import MountModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class PcbShellMainCAD(ManifoldObject):
    layout: Layout
    mount_model: MountModel
    body_parameters: BodyParameters

    def assemble(self) -> manifold3d.Manifold:
        body_cavity = self.deps.stls["build/structure/body/cad/body_cavity.stl"]
        mount_body = self.deps.stls["build/switches/socket/mount/cad/body.stl"]

        pcb_shell = body_cavity - mount_body

        mask = manifold3d.Manifold.cube(
            [
                self.mount_model.main_mask_width,
                self.mount_model.main_mask_depth,
                self.mount_model.main_mask_height,
            ],
            center=False,
        ).translate(
            [
                self.mount_model.main_mask_start_x,
                self.mount_model.main_mask_start_y,
                self.mount_model.bottom_z,
            ]
        )

        p = self.mount_model.switches_parameters
        cube_w = p.size + p.border * 2 + p.clearance * 2
        cube_d = p.size + p.border * 2 + p.clearance * 2

        key_cubes = []
        for column in self.layout.grid:
            for key in column:
                cube = (
                    manifold3d.Manifold.cube(
                        [cube_w, cube_d, self.mount_model.main_mask_height],
                        center=True,
                    )
                    .rotate(key.rotation)
                    .translate(key.position)
                )
                key_cubes.append(cube)

        hole_mask = manifold3d.Manifold.batch_boolean(
            key_cubes, manifold3d.OpType.Add
        )

        switch_hole_decorator_shell_grid = self.deps.stls[
            "build/switches/cad/switch_hole_decorator_shell_grid.stl"
        ]
        light_indicator_body_shell = self.deps.stls[
            "build/components/light_indicator/cad/masks/body_shell.stl"
        ]
        screw_hole_mask = self.deps.stls[
            "build/switches/socket/mount/cad/screw_hole_main.stl"
        ]

        return (
            (pcb_shell ^ mask)
            - hole_mask
            + switch_hole_decorator_shell_grid
            - screw_hole_mask
            - light_indicator_body_shell
        )


if __name__ == "__main__":
    pcb_shell_main = injector.get(PcbShellMainCAD)
    pcb_shell_main.program(sys.argv)
