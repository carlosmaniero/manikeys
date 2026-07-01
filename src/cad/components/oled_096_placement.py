from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from models.components.oled_096 import Oled096PlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class Oled096PlacementCAD(ManifoldObject):
    model: Oled096PlacementModel

    def assemble(self) -> manifold3d.Manifold:
        oled = load_stl_to_manifold("build/cad/components/oled_096.stl")
        return oled.rotate([0, 0, 180]).translate(self.model.placement_position)


if __name__ == "__main__":
    placement = injector.get(Oled096PlacementCAD)
    placement.program(sys.argv)
