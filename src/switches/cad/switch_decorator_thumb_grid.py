import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from models.switch_thumb import SwitchThumbModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class SwitchDecoratorThumbGridCAD(ManifoldObject):
    model: SwitchThumbModel

    def assemble(self) -> manifold3d.Manifold:
        decorator = load_stl_to_manifold("build/switches/cad/switch_hole_decorator.stl")
        positions = self.model.get_positions()

        decorators = [decorator.translate(pos) for pos in positions]

        return manifold3d.Manifold.batch_boolean(decorators, manifold3d.OpType.Add)


if __name__ == "__main__":
    switch_decorator_thumb_grid = injector.get(SwitchDecoratorThumbGridCAD)
    switch_decorator_thumb_grid.program(sys.argv)
