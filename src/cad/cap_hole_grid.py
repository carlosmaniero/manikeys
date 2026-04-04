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
class CapHoleGridCAD(ManifoldObject):
    layout: Layout

    def assemble(self) -> manifold3d.Manifold:
        holes = []
        cap_hole = load_stl_to_manifold("build/cad/cap_hole.stl")

        for column in self.layout.grid:
            for key in column:
                hole = cap_hole.rotate(key.rotation).translate(key.position)
                holes.append(hole)

        return manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)


if __name__ == "__main__":
    cap_hole_grid = injector.get(CapHoleGridCAD)
    cap_hole_grid.program(sys.argv)
