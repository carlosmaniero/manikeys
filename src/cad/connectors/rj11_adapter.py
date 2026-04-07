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
class RJ11AdapterCAD(ManifoldObject):
    parameters: Parameters
    model: RJ11Model
    body_model: BodyModel

    @property
    def height(self) -> float:
        return (
            self.model.rj11.socket_height
            - self.model.rj11.bottom_notch_height
            - self.model.rj11.adapter_head_height
        )

    @property
    def socket(self) -> manifold3d.Manifold:
        height = self.model.rj11.socket_height
        diameter = self.model.rj11.adapter_socket_diameter
        radius = diameter / 2

        cylinder = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            center=True,
            circular_segments=120,
        )

        return cylinder.translate(
            [
                self.model.rj11.width / 2 - radius,
                self.model.notch_start_y,
                -self.model.rj11.height / 2 - self.height / 2,
            ]
        )

    @property
    def bottom_pocket(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.bottom_pocket_width,
                self.parameters.body.thickness,
                self.model.bottom_pocket_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.rj11.length / 2
                + self.parameters.body.thickness / 2
                + self.model.rj11.error_margin,
                self.model.bottom_pocket_height / 2
                - self.model.rj11.height
                - self.height / 2,
            ]
        )

    @property
    def main_block(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.width,
                self.model.rj11.length + self.parameters.body.thickness * 2,
                self.model.rj11.height,
            ],
            center=True,
        )

    @property
    def body(self) -> manifold3d.Manifold:
        return (
            self.main_block
            - self.bottom_notch_mask
            - self.body_mask
            - self.inner_mask
        )

    @property
    def body_mask(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.rj11.width + self.model.rj11.error_margin * 2,
                self.model.rj11.length + self.model.rj11.error_margin * 2,
                self.model.rj11.height,
            ],
            center=True,
        )

    @property
    def bottom_notch_mask(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.rj11.width + self.model.rj11.error_margin * 2,
                self.model.rj11.bottom_notch_length,
                self.model.rj11.bottom_notch_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.notch_start_y,
                (self.model.rj11.height - self.model.rj11.bottom_notch_height)
                / -2,
            ]
        )

    @property
    def inner_mask(self) -> manifold3d.Manifold:
        padding_bottom = self.model.rj11.inner_paddings[2]
        width = self.model.inner_width + self.model.rj11.error_margin * 2
        height = (
            self.model.inner_height
            + self.model.rj11.error_margin * 4
            + padding_bottom / 2
        )

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
                self.model.rj11.inner_length / 2
                + self.model.rj11.error_margin / 2,
                -self.model.rj11.error_margin * 2,
            ]
        )

    @property
    def width(self) -> float:
        return self.model.rj11.width + self.parameters.body.thickness * 2

    @property
    def bottom_base(self) -> manifold3d.Manifold:
        length = (
            self.model.rj11.bottom_notch_start_y
            + self.model.rj11.bottom_notch_length
            + self.parameters.body.thickness
        )

        return manifold3d.Manifold.cube(
            [
                self.width,
                length,
                self.height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.rj11.length / 2
                - length / 2
                + self.parameters.body.thickness,
                -self.model.rj11.height / 2 - self.height / 2,
            ]
        )

    @property
    def bottom_notch(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.rj11.width + self.parameters.body.thickness * 2,
                self.model.rj11.bottom_notch_length
                - self.model.rj11.error_margin * 2,
                self.model.rj11.bottom_notch_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.notch_start_y,
                self.model.rj11.bottom_notch_height / 2
                - self.model.rj11.height / 2,
            ]
        )

    @property
    def sockets(self) -> manifold3d.Manifold:
        return self.socket + self.socket.mirror([1, 0, 0])

    def assemble(self) -> manifold3d.Manifold:
        max_x = self.width / 2
        max_y = self.model.rj11.length / 2 + self.parameters.body.thickness
        return (
            self.bottom_base
            + self.body
            + self.bottom_notch
            - self.sockets
            - self.bottom_pocket
        ).translate(
            [
                self.body_model.end_x() - self.parameters.body.fillet - max_x,
                self.body_model.end_y() - max_y,
                self.body_model.bottom_z
                + self.parameters.body.thickness
                + self.model.rj11.height / 2
                + self.height,
            ]
        )


if __name__ == "__main__":
    adapter = injector.get(RJ11AdapterCAD)
    adapter.program(sys.argv)
