from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from models.components.light_indicator.main_body import MainBodyModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject
from models.parameters import Parameters


@singleton
@inject
@dataclass
class BodyMask(ManifoldObject):
    parameters: Parameters
    indicator_model: MainBodyModel
    body_model: BodyModel

    @property
    def height(self) -> float:
        return self.indicator_model.margin_thickness * 2

    @property
    def body_hull(self) -> manifold3d.Manifold:
        r = self.indicator_model.body_depth / 2

        corner_cyl = manifold3d.Manifold.cylinder(
            height=self.height,
            radius_low=r - 0.1,
            radius_high=r - 0.1,
            center=True,
            circular_segments=32,
        )

        corners = (
            corner_cyl.translate(
                [
                    self.indicator_model.left_edge + r,
                    -self.indicator_model.body_depth / 2 + r,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    self.indicator_model.right_edge - r,
                    -self.indicator_model.body_depth / 2 + r,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    self.indicator_model.left_edge + r,
                    self.indicator_model.body_depth / 2 - r,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    self.indicator_model.right_edge - r,
                    self.indicator_model.body_depth / 2 - r,
                    0,
                ]
            )
        )

        return manifold3d.Manifold.hull(corners)

    def assemble(self) -> manifold3d.Manifold:
        return self.body_hull.rotate(
            self.indicator_model.placement_rotation
        ).translate(self.indicator_model.placement_translation)


if __name__ == "__main__":
    body_mask = injector.get(BodyMask)
    body_mask.program(sys.argv)
