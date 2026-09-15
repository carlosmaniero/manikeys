from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from connectors.rj45.model import RJ45PlacementModel


@singleton
@inject
@dataclass
class RJ45AdapterPlacementCAD(ManifoldObject):
    model: RJ45PlacementModel

    def assemble(self) -> manifold3d.Manifold:
        adapter = self.deps.stls["build/connectors/rj45/cad/adapter.stl"]
        return (
            adapter.rotate([0, 180, 0])
            .rotate([0, 0, -90])
            .translate(self.model.translation_coords)
        )


if __name__ == "__main__":
    adapter_placement = injector.get(RJ45AdapterPlacementCAD)
    adapter_placement.program(sys.argv)
