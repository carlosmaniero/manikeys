from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from core.manifold_ext.helpers import path_extrude
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class ColCablePathCAD(ManifoldObject):
    body_model: BodyModel

    @property
    def path(self) -> list[list[float]]:
        x = self.body_model.end_x()
        start_y = self.body_model.divider_y
        end_y = self.body_model.end_y()
        z = self.body_model.bottom_z
        return [[x, start_y, z], [x, end_y, z]]

    def assemble(self) -> manifold3d.Manifold:
        radius = 2
        square = manifold3d.CrossSection.square(
            [radius + 2, radius + 2], center=True
        )

        return path_extrude(square, self.path)


if __name__ == "__main__":
    cable_path = injector.get(ColCablePathCAD)
    cable_path.program(sys.argv)
