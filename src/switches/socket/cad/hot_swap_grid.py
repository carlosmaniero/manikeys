import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import Layout
from models.switch_thumb import SwitchThumbModel
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from core.loader import load_stl_to_manifold
from switches.socket.mount.models import MountModel
from models.parameters import SwitchesParameters


@singleton
@inject
@dataclass
class HotSwapGridCAD(ManifoldObject):
    layout: Layout
    cad_thump: SwitchThumbModel
    mount_model: MountModel
    switches_parameters: SwitchesParameters

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        hot_swap = load_stl_to_manifold(
            "build/switches/socket/cad/hot_swap.stl"
        ).rotate([180, 0, 180])

        decorator_top = self.switches_parameters.outer.thickness
        main_offset = [0, 0, decorator_top + self.mount_model.offset]
        hot_swap_main = hot_swap.translate(main_offset)

        thumb_offset = [0, 0, decorator_top + self.mount_model.offset]
        hot_swap_thumb = hot_swap.translate(thumb_offset)

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    hot_swap_main.rotate(key.rotation).translate(key.position)
                )

        for position in self.cad_thump.get_positions():
            grid.append(hot_swap_thumb.translate(position))

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    hot_swap_grid = injector.get(HotSwapGridCAD)
    hot_swap_grid.program(sys.argv)
