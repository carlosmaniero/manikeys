import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.cap_thumb import CapThumbModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class CapThumbHoleCAD(ManifoldObject):
    model: CapThumbModel

    def assemble(self) -> manifold3d.Manifold:
        hole = load_stl_to_manifold("build/cad/cap_hole.stl")
        positions = self.model.get_positions()

        holes = [hole.translate(pos) for pos in positions]

        return manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)


if __name__ == "__main__":
    cap_thumb_hole = injector.get(CapThumbHoleCAD)
    cap_thumb_hole.program(sys.argv)
