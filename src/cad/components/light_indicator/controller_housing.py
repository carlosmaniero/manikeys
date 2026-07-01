from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from models.components.light_indicator.led import Led
from models.components.light_indicator.main_body import MainBodyModel
from core.manifold_ext.object import ManifoldObject
from models.parameters import Parameters


@singleton
@inject
@dataclass
class ControllerHousingCad(ManifoldObject):
    model: Led
    parameters: Parameters
    indicator_model: MainBodyModel

    @property
    def body_hull(self) -> manifold3d.Manifold:
        fillet = self.parameters.wall.fillet
        r = min(fillet, self.indicator_model.body_depth / 2 - 0.1)

        corner_cyl = manifold3d.Manifold.cylinder(
            height=self.indicator_model.lid_height,
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
    def pan_lid_mask(self) -> manifold3d.Manifold:
        pcb_mask_radius = (
            self.model.pcb_radius + self.indicator_model.pcb_error / 2
        )
        pcb_mask_diameter = pcb_mask_radius * 2
        offset = pcb_mask_diameter + self.indicator_model.body_thickness / 2

        lid_pcb_radius = pcb_mask_radius + 0.5
        mask_cyl = manifold3d.Manifold.cylinder(
            height=self.indicator_model.pocket_depth + 0.2,
            radius_low=lid_pcb_radius,
            radius_high=lid_pcb_radius,
            center=True,
            circular_segments=32,
        )

        mask = manifold3d.Manifold.hull(
            mask_cyl.translate(
                [-offset - 3 * self.indicator_model.body_thickness, 0, 0]
            )
            + mask_cyl.translate([0, 0, 0])
            + mask_cyl.translate(
                [offset + self.indicator_model.body_thickness, 0, 0]
            )
        )

        return mask.translate(
            [
                0,
                0,
                (
                    self.indicator_model.lid_height
                    - self.indicator_model.pocket_depth
                )
                / 2
                + 0.1,
            ]
        )

    @property
    def pcb_mounting_towers(self) -> manifold3d.Manifold:
        tower_height = self.indicator_model.body_thickness
        tower_dia = 4.0
        tower_radius = tower_dia / 2
        z_bottom = -self.indicator_model.lid_height / 2

        single_tower = manifold3d.Manifold.cylinder(
            height=tower_height,
            radius_low=tower_radius,
            radius_high=tower_radius,
            center=True,
            circular_segments=32,
        ).translate([0, 0, z_bottom - tower_height / 2])

        mask = manifold3d.Manifold()
        hx = self.indicator_model.pcb_width / 2 - 1.26
        hy = self.indicator_model.pcb_length / 2 - 1.26
        for x in [-hx, hx]:
            for y in [-hy, hy]:
                mask += single_tower.translate([x, y, 0])
        return mask

    @property
    def pcb_mounting_holes(self) -> manifold3d.Manifold:
        corner_offset = 1.26
        hole_dia = 1.2
        tower_height = self.indicator_model.body_thickness
        hole_radius = hole_dia / 2
        z_pocket_bottom = (
            self.indicator_model.lid_height / 2
            - self.indicator_model.pocket_depth
        )
        z_tower_bottom = -self.indicator_model.lid_height / 2 - tower_height

        # Hole from pocket floor to tower bottom
        hole_height = z_pocket_bottom - z_tower_bottom

        single_mounting_hole = manifold3d.Manifold.cylinder(
            height=hole_height + 0.2,
            radius_low=hole_radius,
            radius_high=hole_radius,
            center=True,
            circular_segments=16,
        ).translate([0, 0, (z_pocket_bottom + z_tower_bottom) / 2])

        mask = manifold3d.Manifold()
        hx = self.indicator_model.pcb_width / 2 - corner_offset
        hy = self.indicator_model.pcb_length / 2 - corner_offset
        for x in [-hx, hx]:
            for y in [-hy, hy]:
                mask += single_mounting_hole.translate([x, y, 0])
        return mask

    @property
    def lid_screw_holes(self) -> manifold3d.Manifold:
        lid_screw_hole = manifold3d.Manifold.cylinder(
            height=self.indicator_model.lid_height + 0.2,
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
            mask += lid_screw_hole.translate([x, 0, 0])
        return mask

    @property
    def lowerings(self) -> manifold3d.Manifold:
        screw_head_radius = (
            self.parameters.body.m2_screw_head_diameter / 2 + 0.1
        )
        lowering_depth = self.indicator_model.lid_height - 2.0
        z_top = self.indicator_model.lid_height / 2

        lowering_cyl = manifold3d.Manifold.cylinder(
            height=lowering_depth + 0.2,
            radius_low=screw_head_radius,
            radius_high=screw_head_radius,
            center=True,
            circular_segments=32,
        ).translate([0, 0, z_top - lowering_depth / 2 + 0.1])

        mask = manifold3d.Manifold()
        mask += lowering_cyl.translate(
            [self.indicator_model.left_screw_xs[1], 0, 0]
        )
        mask += lowering_cyl.translate(
            [self.indicator_model.right_screw_xs[1], 0, 0]
        )
        return mask

    @property
    def cable_path(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.indicator_model.pcb_width / 4,
                self.indicator_model.body_depth
                - self.indicator_model.body_thickness * 2,
                self.indicator_model.body_thickness * 5,
            ],
            center=True,
        ).translate(
            [
                -self.indicator_model.pcb_width / 2
                - self.indicator_model.pcb_width / 8,
                0,
                0,
            ]
        )

    def assemble(self) -> manifold3d.Manifold:
        return (
            self.body_hull
            + self.pcb_mounting_towers
            - self.pan_lid_mask
            - self.pcb_mounting_holes
            - self.lid_screw_holes
            - self.lowerings
            - self.cable_path
        ).translate([0, 0, -self.indicator_model.body_thickness * 1.5])


if __name__ == "__main__":
    controller_housing = injector.get(ControllerHousingCad)
    controller_housing.program(sys.argv)
