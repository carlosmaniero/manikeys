from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.components.light_indicator.led import Led
from models.components.light_indicator.main_body import MainBodyModel
from manifold_ext.object import ManifoldObject
from models.parameters import Parameters


@singleton
@inject
@dataclass
class MainBodyCad(ManifoldObject):
    model: Led
    params: Parameters
    indicator_model: MainBodyModel

    def create_led_mask(self) -> manifold3d.Manifold:
        pcb_mask_radius = (
            self.model.pcb_radius + self.indicator_model.led_pcb_error / 2
        )
        pcb_height = self.model.pcb_height

        pcb_mask_height = 20
        pcb_mask = (
            manifold3d.Manifold.cylinder(
                height=pcb_mask_height,
                radius_low=pcb_mask_radius,
                radius_high=pcb_mask_radius,
                center=True,
                circular_segments=8,
            )
            .rotate([0, 0, 45 / 2])
            .translate([0, 0, pcb_height - pcb_mask_height / 2])
        )

        led_mask_size = self.model.led_size + self.indicator_model.led_error
        led_mask_height = 10

        led_mask = manifold3d.Manifold.cube(
            [led_mask_size, led_mask_size, led_mask_height],
            center=True,
        ).translate([0, 0, pcb_height + led_mask_height / 2 - 0.1])

        return pcb_mask + led_mask

    @property
    def body_hull(self) -> manifold3d.Manifold:
        fillet = self.params.body.fillet
        r = min(fillet, self.indicator_model.body_depth / 2 - 0.1)

        corner_cyl = manifold3d.Manifold.cylinder(
            height=self.indicator_model.body_thickness,
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
    def masks(self) -> manifold3d.Manifold:
        led_mask = self.create_led_mask()
        z_shift = -self.indicator_model.body_thickness / 2 + 1.0

        mask = manifold3d.Manifold()
        for x in self.indicator_model.led_x_positions:
            mask += led_mask.translate([x, 0, z_shift])
        return mask

    @property
    def screw_holes(self) -> manifold3d.Manifold:
        screw_hole = manifold3d.Manifold.cylinder(
            height=self.indicator_model.body_thickness + 0.2,
            radius_low=self.indicator_model.screw_hole_radius,
            radius_high=self.indicator_model.screw_hole_radius,
            center=True,
            circular_segments=32,
        )

        mask = manifold3d.Manifold()
        for x in (
            self.indicator_model.left_screw_xs
            + self.indicator_model.right_screw_xs
        ):
            mask += screw_hole.translate([x, 0, 0])
        return mask

    @property
    def lowerings(self) -> manifold3d.Manifold:
        screw_head_radius = self.params.body.m2_screw_head_diameter / 2 + 0.1
        screw_head_height = self.params.body.m2_screw_head_height + 0.1
        z_top = self.indicator_model.body_thickness / 2

        # Standard lowering for pan head screws (internal only)
        screw_head_mask = manifold3d.Manifold.cylinder(
            height=screw_head_height,
            radius_low=screw_head_radius,
            radius_high=screw_head_radius,
            center=True,
            circular_segments=32,
        ).translate([0, 0, z_top - screw_head_height / 2 + 0.1])

        mask = manifold3d.Manifold()
        # Internal screws (closest to center)
        mask += screw_head_mask.translate(
            [self.indicator_model.left_screw_xs[0], 0, 0]
        )
        mask += screw_head_mask.translate(
            [self.indicator_model.right_screw_xs[0], 0, 0]
        )

        return mask

    def assemble(self) -> manifold3d.Manifold:
        return self.body_hull - self.masks - self.screw_holes - self.lowerings


if __name__ == "__main__":
    main_body = injector.get(MainBodyCad)
    main_body.program(sys.argv)
