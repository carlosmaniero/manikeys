import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from connectors.rj45.model import RJ45PlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ45AdapterFrontPlacementCAD(ManifoldObject):
    model: RJ45PlacementModel

    def assemble(self) -> M:
        front = load_stl_to_manifold(
            "build/connectors/rj45/cad/adapter_front.stl"
        )
        body = load_stl_to_manifold("build/structure/body/shape.stl")

        placement = front.translate(self.model.translation_coords)

        return placement ^ body


if __name__ == "__main__":
    placement = injector.get(RJ45AdapterFrontPlacementCAD)
    placement.program(sys.argv)
