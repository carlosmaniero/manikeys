import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import Layout
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from switches.socket.mount.models import MountModel
from models.switch_thumb import SwitchThumbModel


@singleton
@inject
@dataclass
class SwitchHoleDecoratorCableMatrixGridCAD(ManifoldObject):
    layout: Layout
    mount_model: MountModel
    switch_thumb_model: SwitchThumbModel

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        matrix = self.deps.stls[
            "build/switches/cad/switch_hole_decorator_cable_matrix.stl"
        ]
        offset = self.mount_model.offset - 0.1

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    matrix.translate([0, 0, offset])
                    .rotate(key.rotation)
                    .translate(key.position)
                )

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    switch_hole_decorator_cable_matrix_grid = injector.get(
        SwitchHoleDecoratorCableMatrixGridCAD
    )
    switch_hole_decorator_cable_matrix_grid.program(sys.argv)
