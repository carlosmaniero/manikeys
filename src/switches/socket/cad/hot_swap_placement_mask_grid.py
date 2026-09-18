import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import Layout, SwitchHoleDecoratorShellModel
from models.switch_thumb import SwitchThumbModel
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from switches.socket.mount.models import MountModel


@singleton
@inject
@dataclass
class HotSwapPlacementMaskGridCAD(ManifoldObject):
    layout: Layout
    switch_thumb_model: SwitchThumbModel
    mount_model: MountModel
    decorator_shell_model: SwitchHoleDecoratorShellModel

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        mask = (
            self.deps.stls[
                "build/switches/socket/cad/hot_swap_placement_mask.stl"
            ]
            .rotate([180, 0, 180])
            .translate(self.decorator_shell_model.mask_translation)
        )
        offset = self.mount_model.offset

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    mask.translate([0, 0, offset])
                    .rotate(key.rotation)
                    .translate(key.position)
                )

        for pos in self.switch_thumb_model.get_positions():
            grid.append(
                mask.translate([0, 0, offset]).scale([-1, 1, 1]).translate(pos)
            )

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    hot_swap_placement_mask_grid = injector.get(HotSwapPlacementMaskGridCAD)
    hot_swap_placement_mask_grid.program(sys.argv)
