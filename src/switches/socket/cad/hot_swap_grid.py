import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import Layout
from models.switch_thumb import SwitchThumbModel
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class HotSwapGridCAD(ManifoldObject):
    layout: Layout
    cad_thump: SwitchThumbModel

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        hot_swap = load_stl_to_manifold("build/switches/socket/cad/hot_swap.stl").rotate(
            [180, 0, 180]
        )

        offset = [0, 0, -2]
        hot_swap = hot_swap.translate(offset)

        for column in self.layout.grid:
            for key in column:
                grid.append(hot_swap.rotate(key.rotation).translate(key.position))

        for position in self.cad_thump.get_positions():
            grid.append(hot_swap.translate(position))

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    hot_swap_grid = injector.get(HotSwapGridCAD)
    hot_swap_grid.program(sys.argv)
