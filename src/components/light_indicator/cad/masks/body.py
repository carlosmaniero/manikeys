from __future__ import annotations
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
class BodyMask(ManifoldObject):
    indicator_model: LightIndicatorModel
    body_model: BodyModel

    @property
    def height(self) -> float:
        return self.indicator_model.margin_thickness * 2

    @property
    def body_hull(self) -> manifold3d.Manifold:
        return rounded_box(
            [
                self.indicator_model.width - 0.2,
                self.indicator_model.body_depth - 0.2,
                self.height,
            ],
            self.indicator_model.body_depth / 2 - 0.1,
        )

    def assemble(self) -> manifold3d.Manifold:
        return self.body_hull.rotate(
            self.indicator_model.placement_rotation
        ).translate(self.indicator_model.placement_translation)


if __name__ == "__main__":
    body_mask = injector.get(BodyMask)
    body_mask.program(sys.argv)
