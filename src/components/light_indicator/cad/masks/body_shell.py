from __future__ import annotations
from globals.wall.parameters import WallParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.helpers import rounded_box
from components.light_indicator.model import LightIndicatorModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class BodyShellMask(ManifoldObject):
    wall_parameters: WallParameters
    indicator_model: LightIndicatorModel
    body_model: BodyModel

    @property
    def height(self) -> float:
        return 100

    @property
    def body_hull(self) -> manifold3d.Manifold:
        t = self.wall_parameters.thickness
        return rounded_box(
            [
                self.indicator_model.width + t,
                self.indicator_model.body_depth + t,
                self.height,
            ],
            self.indicator_model.body_depth / 2 + t / 2,
        )

    def assemble(self) -> manifold3d.Manifold:
        return self.body_hull.rotate(
            self.indicator_model.placement_rotation
        ).translate(self.indicator_model.placement_translation)


if __name__ == "__main__":
    body_shell_mask = injector.get(BodyShellMask)
    body_shell_mask.program(sys.argv)
