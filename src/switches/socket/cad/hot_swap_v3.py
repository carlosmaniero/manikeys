from __future__ import annotations
import sys
from dataclasses import dataclass
from injector import inject, singleton
from manifold3d import Manifold
from globals.wall.parameters import WallParameters
from switches.socket.parameters import HotSwapV2Parameters
from components.light_indicator.parameters import LedParameters
from core.manifold_ext.helpers import rounded_box
from core.manifold_ext.object import ManifoldObject
from core.context import injector


@singleton
@inject
@dataclass
class HotSwapV3CAD(ManifoldObject):
    wall_parameters: WallParameters
    hot_swap_parameters: HotSwapV2Parameters
    led: LedParameters

    def body(self) -> Manifold:
        cube = Manifold.cube(
            [
                self.hot_swap_parameters.cube_size,
                self.hot_swap_parameters.cube_size,
                self.hot_swap_parameters.body_thickness,
            ],
            center=True,
        )
        return cube.translate(
            [
                0,
                0,
                self.hot_swap_parameters.body_thickness / 2,
            ]
        )

    def switch_socket(self) -> Manifold:
        body_holder = Manifold.cube(
            [
                self.hot_swap_parameters.cube_size,
                self.hot_swap_parameters.cube_size,
                self.hot_swap_parameters.switch_socket_height,
            ],
            center=True,
        ).translate(
            [
                0,
                0,
                self.hot_swap_parameters.switch_socket_height,
            ]
        )
        cube = (
            Manifold.cube(
                [
                    self.hot_swap_parameters.switch_socket_width,
                    self.hot_swap_parameters.cube_size,
                    self.hot_swap_parameters.switch_socket_height,
                ],
                center=True,
            )
            + body_holder
        )
        return cube.translate(
            [0, 0, self.hot_swap_parameters.switch_socket_height / 2]
        )

    @property
    def left_pin_hole(self) -> list[float]:
        return [-2.54, 5.08]

    @property
    def right_pin_hole(self) -> list[float]:
        return [3.81, 2.54]

    @property
    def pin_hole_diameter(self) -> float:
        return 1.4

    @property
    def pin_hole_depth(self) -> float:
        return 0.5

    def create_pin_hole(self, point: list[float]) -> Manifold:
        width = self.pin_hole_diameter + 0.02
        depth = self.pin_hole_depth
        height = (
            self.hot_swap_parameters.body_thickness
            + self.hot_swap_parameters.switch_socket_height * 2
        )
        radius = min(depth / 2, width / 2)

        return rounded_box(
            [width, depth, height],
            radius=radius,
            circular_segments=64,
            center=True,
        ).translate([point[0], point[1], height / 2])

    def pin_holes(self) -> Manifold:
        return self.create_pin_hole(self.left_pin_hole) + self.create_pin_hole(
            self.right_pin_hole
        )

    def center_hole(self) -> Manifold:
        height = (
            self.hot_swap_parameters.body_thickness
            + self.hot_swap_parameters.switch_socket_height * 2
        )
        return Manifold.cylinder(
            height,
            self.hot_swap_parameters.center_hole_radius,
            center=True,
            circular_segments=64,
        ).translate([0, 0, height / 2])

    @property
    def awg22_wire_radius(self) -> float:
        return 0.35

    def create_wire_hole(self, pin_point: list[float]) -> Manifold:
        height = (
            self.hot_swap_parameters.body_thickness
            + self.hot_swap_parameters.switch_socket_height * 2
        ) * 2
        wire_y = pin_point[1] + self.awg22_wire_radius
        return Manifold.cylinder(
            height,
            self.awg22_wire_radius,
            center=True,
            circular_segments=64,
        ).translate([pin_point[0], wire_y, height / 2])

    def create_end_wire_hole(self, pin_point: list[float]) -> Manifold:
        height = (
            self.hot_swap_parameters.body_thickness
            + self.hot_swap_parameters.switch_socket_height * 2
        ) * 2
        end_y = self.hot_swap_parameters.cube_size / 2
        return Manifold.cylinder(
            height,
            self.awg22_wire_radius,
            center=True,
            circular_segments=64,
        ).translate([pin_point[0], end_y, height / 2])

    def create_wire_channel(self, pin_point: list[float]) -> Manifold:
        height = self.awg22_wire_radius * 2
        wire_y = pin_point[1] + self.awg22_wire_radius
        end_y = self.hot_swap_parameters.cube_size / 2

        start_cyl = Manifold.cylinder(
            height,
            self.awg22_wire_radius,
            center=True,
            circular_segments=64,
        ).translate([pin_point[0], wire_y, height / 2])

        end_cyl = Manifold.cylinder(
            height,
            self.awg22_wire_radius,
            center=True,
            circular_segments=64,
        ).translate([pin_point[0], end_y, height / 2])

        return Manifold.hull(start_cyl + end_cyl)

    def wire_channels(self) -> Manifold:
        return self.create_wire_channel(
            self.left_pin_hole
        ) + self.create_wire_channel(self.right_pin_hole)

    def wire_holes(self) -> Manifold:
        return (
            self.create_wire_hole(self.left_pin_hole)
            + self.create_wire_hole(self.right_pin_hole)
            + self.create_end_wire_hole(self.left_pin_hole)
            + self.create_end_wire_hole(self.right_pin_hole)
            + self.wire_channels()
        )

    def assemble(self) -> Manifold:
        return (
            self.body()
            + self.switch_socket()
            - self.pin_holes()
            - self.center_hole()
            - self.wire_holes()
        )


if __name__ == "__main__":
    hot_swap_v3 = injector.get(HotSwapV3CAD)
    hot_swap_v3.program(sys.argv)
