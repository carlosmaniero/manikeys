import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import Layout, SwitchHoleDecoratorShellModel
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from switches.socket.mount.models import MountModel
from models.switch_thumb import SwitchThumbModel


@singleton
@inject
@dataclass
class SwitchHoleDecoratorCableMatrixPocketGridCAD(ManifoldObject):
    layout: Layout
    mount_model: MountModel
    switch_thumb_model: SwitchThumbModel
    model: SwitchHoleDecoratorShellModel

    @property
    def pocket(self) -> manifold3d.Manifold:
        hole = manifold3d.Manifold.cube(self.model.block_hole_size, center=True)
        return manifold3d.Manifold.batch_boolean(
            [hole.translate(pos) for pos in self.model.block_hole_translations],
            manifold3d.OpType.Add,
        )

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        pocket = self.pocket
        offset = self.mount_model.offset

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    pocket.translate([0, 0, offset])
                    .rotate(key.rotation)
                    .translate(key.position)
                )

        for pos in self.switch_thumb_model.get_positions():
            grid.append(
                pocket.translate([0, 0, offset])
                .scale([-1, 1, 1])
                .translate(pos)
            )

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    switch_hole_decorator_cable_matrix_pocket_grid = injector.get(
        SwitchHoleDecoratorCableMatrixPocketGridCAD
    )
    switch_hole_decorator_cable_matrix_pocket_grid.program(sys.argv)
