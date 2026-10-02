from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from switches.socket.mount.models import PcbShellHandModel


@singleton
@inject
@dataclass
class PcbShellHandCAD(ManifoldObject):
    model: PcbShellHandModel

    def assemble(self) -> manifold3d.Manifold:
        body_cavity = self.deps.stls["build/structure/body/cad/body_cavity.stl"]
        mount_cavity = self.deps.stls[
            "build/switches/socket/mount/cad/cavity_pcb_shell_main_bottom.stl"
        ]
        switch_hole_decorator_shell_grid = self.deps.stls[
            "build/switches/cad/switch_hole_decorator_shell_grid.stl"
        ]
        oled_placement_body_mask = self.deps.stls[
            "build/components/oled_096/cad/masks/placement_body.stl"
        ]
        oled_lid = self.deps.stls["build/components/oled_096/cad/lid.stl"]
        screw_clearance = self.deps.stls[
            "build/switches/socket/mount/cad/screw_clearance.stl"
        ]

        pcb_shell = body_cavity - mount_cavity

        mask = manifold3d.Manifold.cube(
            self.model.size,
            center=True,
        ).translate(self.model.position)

        top_key_cubes = []
        full_key_cubes = []
        for pos in self.model.positions:
            top_cube = manifold3d.Manifold.cube(
                self.model.cube_top_size,
                center=True,
            ).translate([pos[0], pos[1], self.model.top_cutout_center_z])
            top_key_cubes.append(top_cube)

            full_cube = manifold3d.Manifold.cube(
                self.model.cube_std_size,
                center=True,
            ).translate(pos)
            full_key_cubes.append(full_cube)

        top_hole_mask = manifold3d.Manifold.batch_boolean(
            top_key_cubes, manifold3d.OpType.Add
        )
        full_hole_mask = manifold3d.Manifold.batch_boolean(
            full_key_cubes, manifold3d.OpType.Add
        )

        positioned_oled_lid = (
            oled_lid.translate(self.model.oled_lid_local_coords)
            .rotate([0, 0, 180])
            .translate(self.model.oled_placement_position)
        )

        return (
            pcb_shell
            - top_hole_mask
            - full_hole_mask
            + switch_hole_decorator_shell_grid
            - oled_placement_body_mask
            + positioned_oled_lid
            - screw_clearance
        ) ^ mask


if __name__ == "__main__":
    pcb_shell_hand = injector.get(PcbShellHandCAD)
    pcb_shell_hand.program(sys.argv)
