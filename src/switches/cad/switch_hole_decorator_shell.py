from __future__ import annotations
import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from switches.model import SwitchHoleDecoratorShellModel
from globals.wall.parameters import WallParameters
from core.manifold_ext.helpers import rounded_box
from core.manifold_ext.object import ManifoldObject
from core.context import injector


@singleton
@inject
@dataclass
class SwitchHoleDecoratorShellCAD(ManifoldObject):
    model: SwitchHoleDecoratorShellModel
    wall_parameters: WallParameters

    @property
    def body(self) -> manifold3d.Manifold:
        return rounded_box(
            self.model.cube_size, self.wall_parameters.thickness
        ).translate(self.model.translation)

    @property
    def switch_hole(self) -> manifold3d.Manifold:
        return self.deps.stls["build/switches/cad/switch_hole.stl"]

    @property
    def block_hole(self) -> manifold3d.Manifold:
        hole = manifold3d.Manifold.cube(self.model.block_hole_size, center=True)
        return manifold3d.Manifold.batch_boolean(
            [hole.translate(pos) for pos in self.model.block_hole_translations],
            manifold3d.OpType.Add,
        )

    def assemble(self) -> manifold3d.Manifold:
        return self.body - self.switch_hole - self.block_hole


if __name__ == "__main__":
    switch_hole_decorator_shell = injector.get(SwitchHoleDecoratorShellCAD)
    switch_hole_decorator_shell.program(sys.argv)
