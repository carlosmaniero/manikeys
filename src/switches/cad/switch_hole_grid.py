import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import Layout
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class SwitchHoleGridCAD(ManifoldObject):
    layout: Layout

    def assemble(self) -> manifold3d.Manifold:
        holes = []
        switch_hole = load_stl_to_manifold("build/switches/cad/switch_hole.stl")

        for column in self.layout.grid:
            for key in column:
                hole = switch_hole.rotate(key.rotation).translate(key.position)
                holes.append(hole)

        return manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)


if __name__ == "__main__":
    switch_hole_grid = injector.get(SwitchHoleGridCAD)
    switch_hole_grid.program(sys.argv)
