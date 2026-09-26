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

        divider_y = self.mount_model.divider_y
        height = self.mount_model.sphere.highest + self.body_parameters.height

        fillet = self.mount_model.wall_parameters.fillet
        thickness = self.mount_model.wall_parameters.thickness

        start_x = self.mount_model.start_x() + fillet
        start_y = self.mount_model.divider_y + fillet - thickness
        width = self.mount_model.width - fillet * 2
        depth = self.mount_model.end_y() - fillet - start_y + thickness

        mask = manifold3d.Manifold.cube(
            [
                width,
                depth,
                height * 2,
            ],
            center=False,
        ).translate(
            [
                start_x,
                start_y,
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
                        [cube_w, cube_d, height * 2], center=True
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

        return (pcb_shell ^ mask) - hole_mask + switch_hole_decorator_shell_grid


if __name__ == "__main__":
    pcb_shell_main = injector.get(PcbShellMainCAD)
    pcb_shell_main.program(sys.argv)
