from __future__ import annotations
from globals.wall.parameters import WallParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
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
        r_comp = self.indicator_model.body_depth / 2
        r_mask = r_comp + self.wall_parameters.thickness / 2

        corner_cyl = manifold3d.Manifold.cylinder(
            height=self.height,
            radius_low=r_mask,
            radius_high=r_mask,
            center=True,
            circular_segments=32,
        )

        corners = (
            corner_cyl.translate(
                [
                    self.indicator_model.left_edge + r_comp,
                    -self.indicator_model.body_depth / 2 + r_comp,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    self.indicator_model.right_edge - r_comp,
                    -self.indicator_model.body_depth / 2 + r_comp,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    self.indicator_model.left_edge + r_comp,
                    self.indicator_model.body_depth / 2 - r_comp,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    self.indicator_model.right_edge - r_comp,
                    self.indicator_model.body_depth / 2 - r_comp,
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
    body_shell_mask = injector.get(BodyShellMask)
    body_shell_mask.program(sys.argv)
