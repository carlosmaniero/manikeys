from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from assembly.base_plate.model import BasePlateModel


@singleton
@inject
@dataclass
class BasePlateMaskCAD(ManifoldObject):
    model: BasePlateModel

    def assemble(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            self.model.mask_dimensions,
            center=False,
        ).translate(self.model.mask_coords)


if __name__ == "__main__":
    mask = injector.get(BasePlateMaskCAD)
    mask.program(sys.argv)
