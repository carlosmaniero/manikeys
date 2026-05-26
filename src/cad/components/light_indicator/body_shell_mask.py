from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.components.light_indicator.main_body import MainBodyModel
from models.body import BodyModel
from manifold_ext.object import ManifoldObject
from models.parameters import Parameters
from cad.components.light_indicator.transformations.placement import (
    LightIndicatorPlacement,
)


@singleton
@inject
@dataclass
class BodyShellMask(ManifoldObject):
    parameters: Parameters
    indicator_model: MainBodyModel
    body_model: BodyModel
    placement: LightIndicatorPlacement

    @property
    def height(self) -> float:
        return 100

    @property
    def body_hull(self) -> manifold3d.Manifold:
        r = self.indicator_model.body_depth / 2 + self.parameters.body.thickness

        corner_cyl = manifold3d.Manifold.cylinder(
            height=self.height,
            radius_low=r,
            radius_high=r,
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
        return self.placement.position_on_the_body(self.body_hull)


if __name__ == "__main__":
    body_shell_mask = injector.get(BodyShellMask)
    body_shell_mask.program(sys.argv)
