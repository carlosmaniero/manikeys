from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from structure.body.parameters import BodyParameters
from switches.model import Layout
from switches.socket.mount.models import MountModel
from switches.socket.mount.parameters import PcbShellMainParameters
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class PcbShellMainCAD(ManifoldObject):
    layout: Layout
    mount_model: MountModel
    body_parameters: BodyParameters
    parameters: PcbShellMainParameters

    def assemble(self) -> manifold3d.Manifold:
        body_cavity = self.deps.stls["build/structure/body/cad/body_cavity.stl"]
        mount_cavity = self.deps.stls[
            "build/switches/socket/mount/cad/cavity_pcb_shell_main_bottom.stl"
        ]

        pcb_shell = body_cavity - mount_cavity

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
        cube_w_std = p.size + p.border * 2 + p.clearance * 2
        cube_d_std = p.size + p.border * 2 + p.clearance * 2

        cube_w_top = cube_w_std + self.parameters.cutout_extra_size
        cube_d_top = cube_d_std + self.parameters.cutout_extra_size

        decorator_bottom_z = -(p.thickness - p.outer.thickness)
        decorator_height = p.thickness - p.clearance
        decorator_top_z = (
            self.mount_model.offset + decorator_bottom_z + decorator_height
        )

        mask_top_z = (
            self.mount_model.bottom_z + self.mount_model.main_mask_height
        )
        top_cutout_height = mask_top_z - decorator_top_z

        top_key_cubes = []
        full_key_cubes = []
        for column in self.layout.grid:
            for key in column:
                top_cube = (
                    manifold3d.Manifold.cube(
                        [
                            cube_w_top,
                            cube_d_top,
                            top_cutout_height,
                        ],
                        center=True,
                    )
                    .translate([0, 0, decorator_top_z + top_cutout_height / 2])
                    .rotate(key.rotation)
                    .translate(key.position)
                )
                top_key_cubes.append(top_cube)

                full_cube = (
                    manifold3d.Manifold.cube(
                        [
                            cube_w_std,
                            cube_d_std,
                            self.mount_model.main_mask_height,
                        ],
                        center=True,
                    )
                    .rotate(key.rotation)
                    .translate(key.position)
                )
                full_key_cubes.append(full_cube)

        top_hole_mask = manifold3d.Manifold.batch_boolean(
            top_key_cubes, manifold3d.OpType.Add
        )
        full_hole_mask = manifold3d.Manifold.batch_boolean(
            full_key_cubes, manifold3d.OpType.Add
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
            - top_hole_mask
            - full_hole_mask
            + switch_hole_decorator_shell_grid
            - screw_hole_mask
            - light_indicator_body_shell
        ).translate([0, 0, -0.1])


if __name__ == "__main__":
    pcb_shell_main = injector.get(PcbShellMainCAD)
    pcb_shell_main.program(sys.argv)
