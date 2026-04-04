import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from models.layout import Layout
from models.cap_thumb import CapThumbModel
from manifold_ext.object import ManifoldObject
from context import injector
from loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class SocketGrid(ManifoldObject):
    layout: Layout
    cad_thump: CapThumbModel

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        cap = load_stl_to_manifold("build/cad/socket_adapter.stl").rotate(
            [180, 0, 180]
        )

        offset = [0, 0, -2]
        cap = cap.translate(offset)

        for column in self.layout.grid:
            for key in column:
                grid.append(cap.rotate(key.rotation).translate(key.position))

        for position in self.cad_thump.get_positions():
            grid.append(cap.translate(position))

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    grid = injector.get(SocketGrid)
    grid.program(sys.argv)
