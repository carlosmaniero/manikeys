from __future__ import annotations
from globals.wall.parameters import WallParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from connectors.rj45.model import RJ45PlacementModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ45PlacementMaskCAD(ManifoldObject):
    wall_parameters: WallParameters
    model: RJ45PlacementModel
    body_model: BodyModel

    @property
    def thickness(self) -> float:
        return self.wall_parameters.thickness

    @property
    def main_block(self) -> manifold3d.Manifold:
        size = [
            self.model.rj45_model.screw_tabs[0] + self.thickness,
            self.model.rj45_model.body[1] + self.thickness,
            self.model.rj45_model.front[2]
            + self.thickness
            + self.body_model.highest,
        ]
        return manifold3d.Manifold.cube(size, center=True).translate(
            [0, 0, self.thickness / 2 - self.body_model.highest / 2]
        )

    def assemble(self) -> manifold3d.Manifold:
        return self.main_block.translate(self.model.translation_coords)


if __name__ == "__main__":
    mask = injector.get(RJ45PlacementMaskCAD)
    mask.program(sys.argv)
