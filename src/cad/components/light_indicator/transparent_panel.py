from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.components.light_indicator.main_body import MainBodyModel
from manifold_ext.object import ManifoldObject
from models.parameters import Parameters


@singleton
@inject
@dataclass
class TransparentPanelCad(ManifoldObject):
    params: Parameters
    indicator_model: MainBodyModel

    @property
    def external_panel(self) -> manifold3d.Manifold:
        x_positions = self.indicator_model.led_x_positions
        offset = 5

        panel_cylinder = manifold3d.Manifold.cylinder(
            3.0,
            2.0,
            center=True,
            circular_segments=64,
        ).translate([0, 0, 2])

        return manifold3d.Manifold.hull(
            panel_cylinder.translate([x_positions[0] - offset, 0, 0])
            + panel_cylinder.translate([x_positions[-1] + offset, 0, 0])
        )

    @property
    def body_hull(self) -> manifold3d.Manifold:
        fillet = self.params.body.fillet
        r = min(fillet, self.indicator_model.body_depth / 2 - 0.1)
        height = 1.0
        thickness = self.indicator_model.body_thickness

        corner_cyl = manifold3d.Manifold.cylinder(
            height=height,
            radius_low=r,
            radius_high=r,
            center=True,
            circular_segments=32,
        )

        left_edge = self.indicator_model.left_edge - thickness * 3
        right_edge = self.indicator_model.right_edge + thickness * 3

        corners = (
            corner_cyl.translate(
                [
                    left_edge + r,
                    -self.indicator_model.body_depth / 2 + r,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    right_edge - r,
                    -self.indicator_model.body_depth / 2 + r,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    left_edge + r,
                    self.indicator_model.body_depth / 2 - r,
                    0,
                ]
            )
            + corner_cyl.translate(
                [
                    right_edge - r,
                    self.indicator_model.body_depth / 2 - r,
                    0,
                ]
            )
        )

        return manifold3d.Manifold.hull(corners)

    @property
    def screw_holes(self) -> manifold3d.Manifold:
        height = 1.0
        thickness = self.indicator_model.body_thickness
        screw_gap = thickness * 3

        screw_hole = manifold3d.Manifold.cylinder(
            height=height + 0.2,
            radius_low=self.indicator_model.screw_hole_radius,
            radius_high=self.indicator_model.screw_hole_radius,
            center=True,
            circular_segments=32,
        )

        mask = manifold3d.Manifold()
        mask += screw_hole.translate(
            [self.indicator_model.left_screw_xs[1], 0, 0]
        )
        mask += screw_hole.translate(
            [self.indicator_model.right_screw_xs[1], 0, 0]
        )

        mask += screw_hole.translate(
            [self.indicator_model.left_screw_xs[1] - screw_gap, 0, 0]
        )
        mask += screw_hole.translate(
            [self.indicator_model.right_screw_xs[1] + screw_gap, 0, 0]
        )
        return mask

    def assemble(self) -> manifold3d.Manifold:
        height = 1.0
        return (
            self.body_hull - self.screw_holes + self.external_panel
        ).translate([0, 0, (self.indicator_model.body_thickness + height) / 2])


if __name__ == "__main__":
    transparent_panel = injector.get(TransparentPanelCad)
    transparent_panel.program(sys.argv)
