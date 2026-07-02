from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from models.components.light_indicator.main_body import MainBodyModel
from core.manifold_ext.object import ManifoldObject
from models.parameters import Parameters
from structure.body.models import BodyModel


@singleton
@inject
@dataclass
class PanelFrameCad(ManifoldObject):
    parameters: Parameters
    indicator_model: MainBodyModel
    body_model: BodyModel

    @property
    def height(self) -> float:
        return self.indicator_model.margin_thickness * 2

    @property
    def panel_hole(self) -> manifold3d.Manifold:
        x_positions = self.indicator_model.led_x_positions
        offset = self.indicator_model.led_pcb_radius / 2

        panel_cylinder = manifold3d.Manifold.cylinder(
            self.height + 0.4,
            self.indicator_model.external_panel_radius
            + self.indicator_model.panel_error,
            center=True,
            circular_segments=64,
        )

        return manifold3d.Manifold.hull(
            panel_cylinder.translate([x_positions[0] - offset, 0, 0])
            + panel_cylinder.translate([x_positions[-1] + offset, 0, 0])
        )

    @property
    def body_hull(self) -> manifold3d.Manifold:
        r = self.indicator_model.body_depth / 2

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

    @property
    def screw_holes(self) -> manifold3d.Manifold:
        screw_hole = manifold3d.Manifold.cylinder(
            height=self.height + 0.2,
            radius_low=self.indicator_model.screw_hole_radius,
            radius_high=self.indicator_model.screw_hole_radius,
            center=True,
            circular_segments=32,
        )

        mask = manifold3d.Manifold()
        for x in [
            self.indicator_model.left_screw_x,
            self.indicator_model.right_screw_x,
        ]:
            mask += screw_hole.translate(
                [x, 0, -self.parameters.wall.thickness]
            )
        return mask

    def assemble(self) -> manifold3d.Manifold:
        return (
            (self.body_hull - self.screw_holes - self.panel_hole)
            .rotate(self.indicator_model.placement_rotation)
            .translate(self.indicator_model.placement_translation)
        )


if __name__ == "__main__":
    panel_frame = injector.get(PanelFrameCad)
    panel_frame.program(sys.argv)
