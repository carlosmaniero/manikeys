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
class SwitchHoleDecoratorGridCAD(ManifoldObject):
    layout: Layout

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        decorator = load_stl_to_manifold(
            "build/switches/cad/switch_hole_decorator.stl"
        )

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    decorator.rotate(key.rotation).translate(key.position)
                )

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    switch_hole_decorator_grid = injector.get(SwitchHoleDecoratorGridCAD)
    switch_hole_decorator_grid.program(sys.argv)
