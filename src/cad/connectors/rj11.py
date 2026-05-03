from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.rj11 import RJ11Model
from models.body import BodyModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ11CAD(ManifoldObject):
    parameters: Parameters
    model: RJ11Model
    body_model: BodyModel

    @property
    def body(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.rj11.width,
                self.model.rj11.length,
                self.model.rj11.height,
            ],
            center=True,
        )

    @property
    def bottom_pocket(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.bottom_pocket_width,
                self.model.bottom_pocket_length,
                self.model.bottom_pocket_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.rj11.length / 2
                - self.model.bottom_pocket_length / 2,
                0,
            ]
        )

    @property
    def top_pocket(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.top_pocket_width,
                self.model.top_pocket_length,
                self.model.top_pocket_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.rj11.length / 2 - self.model.top_pocket_length / 2,
                self.model.rj11.height / 2 - self.model.top_pocket_height / 2,
            ]
        )

    @property
    def inner(self) -> manifold3d.Manifold:
        width = self.model.inner_width
        height = self.model.inner_height

        return manifold3d.Manifold.cube(
            [
                width,
                self.model.rj11.inner_length,
                height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.rj11.length / 2 - self.model.rj11.inner_length / 2,
                self.model.rj11.height / 2
                - self.model.rj11.inner_paddings[0]
                - height / 2,
            ]
        )

    @property
    def bottom_notch(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.rj11.width,
                self.model.rj11.bottom_notch_length,
                self.model.rj11.bottom_notch_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.notch_start_y,
                -self.model.rj11.height / 2
                + self.model.rj11.bottom_notch_height / 2,
            ]
        )

    @property
    def socket(self) -> manifold3d.Manifold:
        height = self.model.rj11.socket_height
        diameter = self.model.rj11.socket_diameter
        radius = diameter / 2

        cylinder = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            center=True,
            circular_segments=120,
        ).translate(
            [
                0,
                -0.5,
                -(self.model.rj11.height + height) / 2
                + self.model.rj11.bottom_notch_height,
            ]
        )

        hole = manifold3d.Manifold.cube(
            [diameter, 0.5, height - 0.5], center=True
        ).translate([0, -0.25, -(self.model.rj11.height + height) / 2])

        return (
            manifold3d.Manifold.hull(cylinder + cylinder.translate([0, 0.5, 0]))
            - hole
        ).translate(
            [
                self.model.rj11.width / 2 - radius - 0.5,
                0.25 + self.model.notch_start_y,
                0,
            ]
        )

    @property
    def sockets(self) -> manifold3d.Manifold:
        return self.socket + self.socket.mirror([1, 0, 0])

    @property
    def height(self) -> float:
        return (
            self.model.rj11.socket_height
            - self.model.rj11.bottom_notch_height
            - self.model.rj11.adapter_head_height
        )

    @property
    def width(self) -> float:
        return self.model.rj11.width + self.parameters.body.thickness * 2

    def assemble(self) -> manifold3d.Manifold:
        max_x = self.width / 2
        max_y = self.model.rj11.length / 2 + self.parameters.body.thickness

        return (
            (
                self.body
                - self.bottom_notch
                - self.inner
                - self.top_pocket
                - self.bottom_pocket
            )
            + self.sockets
        ).translate(
            [
                self.body_model.end_x() - self.parameters.body.fillet - max_x,
                self.body_model.end_y()
                - max_y
                + self.parameters.body.thickness
                - self.model.rj11.error_margin * 2,
                self.body_model.bottom_z
                + self.parameters.body.thickness
                + self.model.rj11.height / 2
                + self.height,
            ]
        )


if __name__ == "__main__":
    adapter = injector.get(RJ11CAD)
    adapter.program(sys.argv)
