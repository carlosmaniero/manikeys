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
    def width(self) -> float:
        return self.model.rj11.width + self.parameters.body.thickness * 2

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
    def main_block(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.width,
                self.model.rj11.length
                + self.parameters.body.thickness
                + self.model.rj11.error_margin * 2,
                self.model.rj11.height,
            ],
            center=True,
        ).translate(
            [
                0,
                -self.parameters.body.thickness / 2
                + self.model.rj11.error_margin * 2,
                0,
            ]
        )

    @property
    def body(self) -> manifold3d.Manifold:
        return self.main_block - self.body_mask

    @property
    def body_mask(self) -> manifold3d.Manifold:
        mask = manifold3d.Manifold.cube(
            [
                self.model.rj11.width + self.model.rj11.error_margin * 2,
                self.model.rj11.length + self.model.rj11.error_margin * 2,
                self.model.rj11.height + self.body_model.highest,
            ],
            center=True,
        ).translate(
            [0, self.parameters.body.thickness, self.body_model.highest / 2]
        )

        return mask + mask.translate([0, -self.parameters.body.thickness, 0])

    @property
    def bottom_base(self) -> manifold3d.Manifold:
        length = (
            self.model.rj11.bottom_notch_start_y
            + self.model.rj11.bottom_notch_length
        )

        return manifold3d.Manifold.cube(
            [
                self.width,
                length + self.model.rj11.error_margin * 2,
                self.height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.model.rj11.length / 2
                - length / 2
                + self.model.rj11.error_margin * 2,
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
            self.body + self.bottom_base + self.bottom_notch - self.sockets
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
    adapter = injector.get(RJ11AdapterCAD)
    adapter.program(sys.argv)
