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
class SwitchThumbHoleCAD(ManifoldObject):
    model: SwitchThumbModel

    def assemble(self) -> manifold3d.Manifold:
        hole = load_stl_to_manifold("build/switches/cad/switch_hole.stl")
        positions = self.model.get_positions()

        holes = [hole.translate(pos) for pos in positions]

        return manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)


if __name__ == "__main__":
    switch_thumb_hole = injector.get(SwitchThumbHoleCAD)
    switch_thumb_hole.program(sys.argv)
