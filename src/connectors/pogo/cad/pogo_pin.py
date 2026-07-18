from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.helpers import capsule
from connectors.pogo.models import PogoPinModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class PogoPinCAD(ManifoldObject):
    model: PogoPinModel
    body_model: BodyModel

    @property
    def main_body(self) -> manifold3d.Manifold:
        return capsule(
            [
                self.model.body_length,
                self.model.body_width,
                self.model.body_height,
            ],
            circular_segments=60,
        )

    @property
    def flanges(self) -> manifold3d.Manifold:
        return capsule(
            [
                self.model.flange_full_length,
                self.model.body_width,
                self.model.flange_thickness,
            ],
            circular_segments=60,
        ).translate(
            [
                0,
                0,
                self.model.flange_z_offset,
            ]
        )

    @property
    def mounting_holes(self) -> manifold3d.Manifold:
        radius = self.model.mounting_hole_diameter / 2
        distance = self.model.mounting_hole_distance
        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=self.model.flange_thickness + 0.5,
            circular_segments=60,
            center=True,
        ).translate(
            [
                0,
                0,
                self.model.flange_z_offset,
            ]
        )

        return hole.translate([distance / 2, 0, 0]) + hole.translate(
            [-distance / 2, 0, 0]
        )

    @property
    def pins(self) -> manifold3d.Manifold:
        tip_radius = self.model.pin_tip_diameter / 2
        tip_height = self.model.pin_height
        pitch = self.model.pin_pitch
        count = self.model.pin_count

        tip = manifold3d.Manifold.cylinder(
            radius_low=tip_radius,
            radius_high=tip_radius,
            height=tip_height,
            circular_segments=30,
            center=True,
        ).translate([0, 0, tip_height / 2 - self.model.body_height / 2])

        tail_radius = self.model.solder_tail_diameter / 2
        tail_height = self.model.solder_tail_length
        tail = manifold3d.Manifold.cylinder(
            radius_low=tail_radius,
            radius_high=tail_radius,
            height=tail_height,
            circular_segments=30,
            center=True,
        ).translate([0, 0, -tail_height / 2 - self.model.body_height / 2])

        pin_unit = tip + tail

        start_x = self.model.pins_start_x
        pins = pin_unit.translate([start_x, 0, 0])
        for i in range(1, count):
            pins += pin_unit.translate([start_x + i * pitch, 0, 0])

        return pins

    @property
    def magnets(self) -> manifold3d.Manifold:
        radius = 1.5
        height = 3.0
        distance = self.model.magnet_distance

        magnet = manifold3d.Manifold.cylinder(
            radius_low=radius, radius_high=radius, height=height, center=True
        ).translate([0, 0, -self.model.body_height / 2 + height / 2])

        return magnet.translate([distance / 2, 0, 0]) + magnet.translate(
            [-distance / 2, 0, 0]
        )

    def assemble(self) -> manifold3d.Manifold:
        return (
            self.main_body
            + self.flanges
            - self.mounting_holes
            - self.magnets
            + self.pins
        )


if __name__ == "__main__":
    pogo = injector.get(PogoPinCAD)
    pogo.program(sys.argv)
