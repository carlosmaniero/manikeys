from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass, field
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ11CAD(ManifoldObject):
    parameters: Parameters

    # TODO: move to parameters
    width: float = field(init=False, default=11)
    height: float = field(init=False, default=11.5)
    length: float = field(init=False, default=18.2)
    bottom_notch_length: float = field(init=False, default=6)
    bottom_notch_height: float = field(init=False, default=0.5)
    bottom_notch_start_y: float = field(init=False, default=5)
    inner_paddings: list[float] = field(
        init=False, default_factory=lambda: [2.0, 1.5, 3.0, 1.5]
    )
    inner_length: float = field(init=False, default=12)

    @property
    def notch_start_y(self) -> float:
        return (
            self.length / 2
            - self.bottom_notch_start_y
            - self.bottom_notch_length / 2
        )

    @property
    def body(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [self.width, self.length, self.height], center=True
        )

    @property
    def inner_width(self) -> float:
        return self.width - self.inner_paddings[1] - self.inner_paddings[3]

    @property
    def inner_height(self) -> float:
        return self.height - self.inner_paddings[0] - self.inner_paddings[2]

    @property
    def top_pocket_width(self) -> float:
        return self.width - 3.25 * 2

    @property
    def top_pocket_height(self) -> float:
        return self.height - 1

    @property
    def top_pocket_length(self) -> float:
        return 3

    @property
    def bottom_pocket_width(self) -> float:
        return self.width - 4 * 2

    @property
    def bottom_pocket_height(self) -> float:
        return self.height

    @property
    def bottom_pocket_length(self) -> float:
        return 1.5

    @property
    def bottom_pocket(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.bottom_pocket_width,
                self.bottom_pocket_length,
                self.bottom_pocket_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.length / 2 - self.bottom_pocket_length / 2,
                0,
            ]
        )

    @property
    def top_pocket(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.top_pocket_width,
                self.top_pocket_length,
                self.top_pocket_height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.length / 2 - self.top_pocket_length / 2,
                self.height / 2 - self.top_pocket_height / 2,
            ]
        )

    @property
    def inner(self) -> manifold3d.Manifold:
        width = self.inner_width
        height = self.inner_height

        return manifold3d.Manifold.cube(
            [
                width,
                self.inner_length,
                height,
            ],
            center=True,
        ).translate(
            [
                0,
                self.length / 2 - self.inner_length / 2,
                self.height / 2 - self.inner_paddings[0] - height / 2,
            ]
        )

    @property
    def bottom_notch(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [self.width, self.bottom_notch_length, self.bottom_notch_height],
            center=True,
        ).translate(
            [
                0,
                self.notch_start_y,
                -self.height / 2 + self.bottom_notch_height / 2,
            ]
        )

    @property
    def socket(self) -> manifold3d.Manifold:
        height = 4.4
        diameter = 2
        radius = diameter / 2

        cylinder = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            center=True,
            circular_segments=120,
        ).translate(
            [0, -0.5, -(self.height + height) / 2 + self.bottom_notch_height]
        )

        hole = manifold3d.Manifold.cube(
            [diameter, 0.5, height - 0.5], center=True
        ).translate([0, -0.25, -(self.height + height) / 2])

        return (
            manifold3d.Manifold.hull(cylinder + cylinder.translate([0, 0.5, 0]))
            - hole
        ).translate(
            [self.width / 2 - radius - 0.5, 0.25 + self.notch_start_y, 0]
        )

    @property
    def sockets(self) -> manifold3d.Manifold:
        return self.socket + self.socket.mirror([1, 0, 0])

    def assemble(self) -> manifold3d.Manifold:
        return (
            self.body
            - self.bottom_notch
            - self.inner
            - self.top_pocket
            - self.bottom_pocket
        ) + self.sockets


if __name__ == "__main__":
    adapter = injector.get(RJ11CAD)
    adapter.program(sys.argv)
