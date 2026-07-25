from __future__ import annotations
import sys
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from components.female_pin_header.model import FemalePinHeaderModel
from core.manifold_ext.object import ManifoldObject
from components.female_pin_header.cad.female_pin_header_body import (
    FemalePinHeaderBodyBaseCAD,
)
import manifold3d


@singleton
@inject
@dataclass
class FemalePinHeaderBody7CAD(ManifoldObject):
    model: FemalePinHeaderModel

    def assemble(self) -> manifold3d.Manifold:
        base = FemalePinHeaderBodyBaseCAD(self.model)
        return base.create_housing(7)


if __name__ == "__main__":
    female_pin_header = injector.get(FemalePinHeaderBody7CAD)
    female_pin_header.program(sys.argv)
