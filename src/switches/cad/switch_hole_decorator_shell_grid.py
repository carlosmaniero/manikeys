import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import Layout
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from core.loader import load_stl_to_manifold
from switches.socket.mount.models import MountModel


@singleton
@inject
@dataclass
class SwitchHoleDecoratorShellGridCAD(ManifoldObject):
    layout: Layout
    mount_model: MountModel

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        decorator = load_stl_to_manifold(
            "build/switches/cad/switch_hole_decorator_shell.stl"
        )
        offset = self.mount_model.offset

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    decorator.translate([0, 0, offset])
                    .rotate(key.rotation)
                    .translate(key.position)
                )

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    switch_hole_decorator_shell_grid = injector.get(
        SwitchHoleDecoratorShellGridCAD
    )
    switch_hole_decorator_shell_grid.program(sys.argv)
