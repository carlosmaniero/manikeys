from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from switches.socket.mount.models import MountModel
from switches.socket.mount.parameters import PcbShellMainGuideParameters


@singleton
@inject
@dataclass
class PcbShellMainGuideCAD(ManifoldObject):
    mount_model: MountModel
    parameters: PcbShellMainGuideParameters

    def assemble(self) -> manifold3d.Manifold:
        shape = self.deps.stls["build/structure/body/shape.stl"]
        mount_cavity = self.deps.stls[
            "build/switches/socket/mount/cad/cavity_pcb_shell_main_bottom.stl"
        ]
        light_indicator_body_shell = self.deps.stls[
            "build/components/light_indicator/cad/masks/body_shell.stl"
        ]

        thickness = self.parameters.thickness
        clearance = 0.2

        w = self.mount_model.main_mask_width
        d = self.mount_model.main_mask_depth
        h = self.mount_model.main_mask_height

        x = self.mount_model.main_mask_start_x
        y = self.mount_model.main_mask_start_y
        z = self.mount_model.bottom_z

        outer_cube = manifold3d.Manifold.cube(
            [
                w + thickness * 2,
                d + thickness * 2,
                h,
            ],
            center=False,
        ).translate(
            [
                x - thickness,
                y - thickness,
                z,
            ]
        )

        inner_cube = manifold3d.Manifold.cube(
            [
                w + clearance * 2 + thickness,
                d + clearance * 2,
                h,
            ],
            center=False,
        ).translate(
            [
                x - clearance - thickness,
                y - clearance,
                z,
            ]
        )

        guide = outer_cube - inner_cube
        return (guide ^ shape) - mount_cavity - light_indicator_body_shell


if __name__ == "__main__":
    pcb_shell_main_guide = injector.get(PcbShellMainGuideCAD)
    pcb_shell_main_guide.program(sys.argv)
