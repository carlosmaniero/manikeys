from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from connectors.rj45_tabs.model import AdapterPlacementModel


@singleton
@inject
@dataclass
class AdapterPlacementCAD(ManifoldObject):
    model: AdapterPlacementModel

    def assemble(self) -> manifold3d.Manifold:
        adapter = self.deps.stls["build/connectors/rj45_tabs/cad/adapter.stl"]
        body = self.deps.stls["build/structure/body/shape.stl"]
        placement = (
            adapter.rotate([0, 180, 0])
            .rotate([90, 0, -90])
            .translate(self.model.translation_coords)
        )
        return placement ^ body


if __name__ == "__main__":
    adapter_placement = injector.get(AdapterPlacementCAD)
    adapter_placement.program(sys.argv)
