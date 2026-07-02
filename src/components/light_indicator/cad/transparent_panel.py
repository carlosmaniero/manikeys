from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from components.light_indicator.model import LightIndicatorModel
from core.manifold_ext.object import ManifoldObject
from models.parameters import Parameters


@singleton
@inject
@dataclass
class TransparentPanelCad(ManifoldObject):
    params: Parameters
    indicator_model: LightIndicatorModel

    @property
    def external_panel(self) -> manifold3d.Manifold:
        x_positions = self.indicator_model.led_x_positions
        offset = self.indicator_model.led_pcb_radius / 2
        height = self.indicator_model.margin_thickness * 2
        base_height = self.indicator_model.transparent_panel_thickness

        panel_cylinder = manifold3d.Manifold.cylinder(
            height,
            self.indicator_model.external_panel_radius,
            center=True,
            circular_segments=64,
        ).translate([0, 0, (height + base_height) / 2])

        return manifold3d.Manifold.hull(
            panel_cylinder.translate([x_positions[0] - offset, 0, 0])
            + panel_cylinder.translate([x_positions[-1] + offset, 0, 0])
        )

    @property
    def body_hull(self) -> manifold3d.Manifold:
        r = self.indicator_model.body_depth / 2

        corner_cyl = manifold3d.Manifold.cylinder(
            height=self.indicator_model.transparent_panel_thickness,
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
        height = self.indicator_model.margin_thickness

        screw_hole = manifold3d.Manifold.cylinder(
            height=height + 0.2,
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
            mask += screw_hole.translate([x, 0, 0])
        return mask

    def assemble(self) -> manifold3d.Manifold:
        return (
            self.body_hull - self.screw_holes + self.external_panel
        ).translate(
            [
                0,
                0,
                (
                    self.indicator_model.body_thickness
                    + self.indicator_model.transparent_panel_thickness
                )
                / 2,
            ]
        )


if __name__ == "__main__":
    transparent_panel = injector.get(TransparentPanelCad)
    transparent_panel.program(sys.argv)
