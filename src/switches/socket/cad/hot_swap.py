from __future__ import annotations
import sys
from manifold3d import Manifold
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from models.parameters import Parameters
from components.light_indicator.parameters import LedParameters
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class SocketAdapter2CAD(ManifoldObject):
    parameters: Parameters
    led: LedParameters

    def body(self) -> Manifold:
        cube = Manifold.cube(
            [
                self.parameters.hot_swap.cube_size,
                self.parameters.hot_swap.cube_size
                - self.parameters.wall.thickness,
                self.parameters.hot_swap.body_thickness,
            ],
            center=True,
        )
        return cube.translate(
            [
                0,
                self.parameters.wall.thickness / 2,
                self.parameters.hot_swap.body_thickness / 2,
            ]
        )

    def led_placement_pcb(self) -> Manifold:
        return (
            Manifold.cylinder(
                self.led.pcb_height - self.led.pcb_actual_height,
                self.led.pcb_radius,
                self.led.pcb_enty_radius,
                circular_segments=8,
            ).translate([0, 0, self.led.pcb_actual_height])
            + Manifold.cylinder(
                self.led.pcb_height,
                self.led.pcb_radius,
                circular_segments=8,
            )
        ).rotate([0, 0, 22.5])

    def led_placement_top(self) -> Manifold:
        return self.centralize_led_object(
            Manifold.cube(
                [
                    self.parameters.hot_swap.cube_size,
                    self.parameters.hot_swap.cube_size,
                    self.led.pcb_height,
                ],
                center=True,
            )
        ).translate(
            [
                0,
                0,
                self.led.pcb_height / 2,
            ]
        )

    def led_placement_hole(self) -> Manifold:
        return Manifold.cube(
            [
                self.led.led_size,
                self.led.led_size,
                self.parameters.hot_swap.body_thickness,
            ],
            center=True,
        ).translate(
            [
                0,
                0,
                -(self.parameters.hot_swap.body_thickness) / 2,
            ]
        )

    def centralize_led_object(self, obj: Manifold) -> Manifold:
        return obj.translate(
            [
                0,
                -self.parameters.hot_swap.cube_size / 2 + self.led.led_size / 2,
                self.parameters.hot_swap.body_thickness - self.led.pcb_height,
            ]
        )

    def led_placement(self) -> Manifold:
        return self.centralize_led_object(
            self.led_placement_pcb() + self.led_placement_hole()
        )

    def switch_socket(self) -> Manifold:
        body_holder = Manifold.cube(
            [
                self.parameters.hot_swap.cube_size,
                self.parameters.hot_swap.cube_size,
                self.parameters.hot_swap.switch_socket_height,
            ],
            center=True,
        ).translate(
            [
                0,
                0,
                self.parameters.hot_swap.switch_socket_height,
            ]
        )
        cube = (
            Manifold.cube(
                [
                    self.parameters.hot_swap.switch_socket_width,
                    self.parameters.hot_swap.cube_size,
                    self.parameters.hot_swap.switch_socket_height,
                ],
                center=True,
            )
            + body_holder
        )
        return cube.translate(
            [0, 0, self.parameters.hot_swap.switch_socket_height / 2]
        )

    def countersink(
        self,
        big_radius: float,
        hole_radius: float,
        height: float,
        other_height: float = 0.5,
    ) -> Manifold:
        return Manifold.cylinder(
            height, hole_radius, circular_segments=64
        ) + Manifold.cylinder(
            other_height, big_radius, hole_radius, circular_segments=64
        )

    def center_hole(self) -> Manifold:
        return self.countersink(
            self.parameters.hot_swap.center_hole_radius + 1,
            self.parameters.hot_swap.center_hole_radius,
            self.parameters.hot_swap.body_thickness,
        )

    @property
    def left_pin_hole(self) -> list[float]:
        return [-2.54, 5.08]

    @property
    def right_pin_hole(self) -> list[float]:
        return [3.81, 2.54]

    @property
    def pin_hole_diameter(self) -> float:
        return 1.5

    @property
    def soldering_placement(self) -> Manifold:
        return Manifold.sphere(3, circular_segments=64).translate(
            [0, 0, self.parameters.hot_swap.body_thickness + 2]
        )

    def create_pin_hole(self, point: list[float]) -> Manifold:
        diameter = self.pin_hole_diameter
        error = 0.01

        return (
            self.countersink(
                diameter / 2 + error + 0.5,
                diameter / 2 + error,
                self.parameters.hot_swap.body_thickness,
            )
            + self.soldering_placement
        ).translate([point[0], point[1], 0])

    def pin_holes(self) -> Manifold:
        return (
            self.create_pin_hole(self.left_pin_hole)
            + self.create_pin_hole(self.right_pin_hole)
            + self.create_wire_hole(
                [
                    self.parameters.hot_swap.diode_x,
                    self.left_pin_hole[1],
                ]
            )
            + self.create_wire_hole(
                [
                    self.right_pin_hole[0],
                    self.right_pin_hole[1] + 2,
                ]
            )
        )

    def create_wire_hole(self, point: list[float]) -> Manifold:
        cylinder = Manifold.cylinder(
            self.parameters.hot_swap.body_thickness,
            self.pin_hole_diameter / 2,
            circular_segments=64,
        )

        end_position = cylinder.translate([point[0], point[1], 0])

        start_position = cylinder.translate(
            [point[0], self.parameters.hot_swap.cube_size, 0]
        )

        return Manifold.hull(end_position + start_position)

    @property
    def diode_wire_hole_center_x(self) -> float:
        return (
            -self.parameters.hot_swap.cube_size
            + self.led.led_size
            - self.parameters.hot_swap.diode_r / 2
        ) / 2

    def diode(self) -> Manifold:
        border = (
            self.parameters.hot_swap.border
            + self.parameters.hot_swap.offset_fix
        )

        full_height = self.parameters.hot_swap.diode_l + border

        d1 = Manifold.cylinder(
            height=full_height,
            radius_low=self.parameters.hot_swap.diode_r,
            center=True,
            circular_segments=64,
        )

        d2 = Manifold.cylinder(
            height=100,
            radius_low=self.parameters.hot_swap.diode_wire_r,
            center=True,
            circular_segments=64,
        )

        d = d1 + d2

        return d.rotate([90, 0, 0]).translate(
            [
                self.diode_wire_hole_center_x,
                -self.parameters.hot_swap.cube_size / 2
                + full_height / 2
                + self.parameters.wall.thickness,
                self.parameters.hot_swap.body_thickness
                - self.parameters.hot_swap.diode_r
                - self.led.pcb_height,
            ]
        )

    def assemble(self) -> Manifold:
        return (
            self.body()
            + self.led_placement_top()
            + self.switch_socket()
            - self.led_placement()
            - self.center_hole()
            - self.pin_holes()
            - self.diode()
        )


if __name__ == "__main__":
    adapter = injector.get(SocketAdapter2CAD)
    adapter.program(sys.argv)
