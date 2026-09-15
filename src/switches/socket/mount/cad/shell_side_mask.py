from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from globals.wall.parameters import WallParameters
from switches.socket.mount.models import MountModel


from structure.body.screws.models import ScrewPlacementModel


@singleton
@inject
@dataclass
class ShellSideMaskModel:
    mount_model: MountModel
    wall_parameters: WallParameters
    screw_placement_model: ScrewPlacementModel

    @property
    def size(self) -> tuple[float, float, float]:
        width = (
            self.mount_model.width
            - self.screw_placement_model.standoff_size * 4
        )
        depth = self.wall_parameters.fillet
        return (width, depth, self.mount_model.height)

    @property
    def coords(self) -> list[float]:
        return [
            self.mount_model.start_x()
            + self.screw_placement_model.standoff_size * 2,
            self.mount_model.end_y() - self.size[1],
            self.mount_model.bottom_z,
        ]


@singleton
@inject
@dataclass
class ShellSideMaskCAD(ManifoldObject):
    model: ShellSideMaskModel

    def assemble(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            self.model.size, center=False
        ).translate(self.model.coords)


if __name__ == "__main__":
    shell_side_mask = injector.get(ShellSideMaskCAD)
    shell_side_mask.program(sys.argv)
