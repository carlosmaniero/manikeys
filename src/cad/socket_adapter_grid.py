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
class SocketGrid(ManifoldObject):
    layout: Layout
    cad_thump: SwitchThumbModel

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        socket_adapter = load_stl_to_manifold("build/cad/socket_adapter.stl").rotate(
            [180, 0, 180]
        )

        offset = [0, 0, -2]
        socket_adapter = socket_adapter.translate(offset)

        for column in self.layout.grid:
            for key in column:
                grid.append(socket_adapter.rotate(key.rotation).translate(key.position))

        for position in self.cad_thump.get_positions():
            grid.append(socket_adapter.translate(position))

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    grid = injector.get(SocketGrid)
    grid.program(sys.argv)
