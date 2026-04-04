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
class CapThumbCAD(ManifoldObject):
    model: CapThumbModel

    def assemble(self) -> manifold3d.Manifold:
        cap = load_stl_to_manifold("build/cad/cap.stl")
        positions = self.model.get_positions()

        caps = [cap.translate(pos) for pos in positions]

        return manifold3d.Manifold.batch_boolean(caps, manifold3d.OpType.Add)


if __name__ == "__main__":
    cap_thumb = injector.get(CapThumbCAD)
    cap_thumb.program(sys.argv)
