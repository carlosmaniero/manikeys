from __future__ import annotations
import sys
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from components.female_pin_header.cad.female_pin_header import (
    FemalePinHeaderBaseCAD,
)
from components.female_pin_header.model import FemalePinHeaderModel
import manifold3d


@singleton
@inject
@dataclass
class FemalePinHeader4CAD(FemalePinHeaderBaseCAD):
    def assemble(self) -> manifold3d.Manifold:
        return self.create_housing(4)


if __name__ == "__main__":
    female_pin_header = injector.get(FemalePinHeader4CAD)
    female_pin_header.program(sys.argv)
