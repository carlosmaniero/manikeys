import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from models.layout import Layout
from manifold_ext.object import ManifoldObject
from context import injector
from loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class CapGridCAD(ManifoldObject):
    layout: Layout

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        cap = load_stl_to_manifold("build/cad/cap.stl")

        for column in self.layout.grid:
            for key in column:
                grid.append(cap.rotate(key.rotation).translate(key.position))

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    cap_grid = injector.get(CapGridCAD)
    cap_grid.program(sys.argv)
