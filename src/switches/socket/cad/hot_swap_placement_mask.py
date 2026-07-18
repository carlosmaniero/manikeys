from __future__ import annotations
from globals.wall.parameters import WallParameters
from switches.socket.parameters import HotSwapParameters
from models.parameters import SwitchesParameters
import sys
from manifold3d import Manifold
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from components.light_indicator.parameters import LedParameters
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class HotSwapPlacementMaskCAD(ManifoldObject):
    wall_parameters: WallParameters
    hot_swap_parameters: HotSwapParameters
    led: LedParameters
    switches_parameters: SwitchesParameters

    def body(self) -> Manifold:
        clearance = self.hot_swap_parameters.mask_clearance
        cube = Manifold.cube(
            [
                self.switches_parameters.size,
                self.hot_swap_parameters.cube_size
                - self.wall_parameters.thickness
                + clearance,
                self.hot_swap_parameters.body_thickness + clearance,
            ],
            center=True,
        )
        return cube.translate(
            [
                0,
                self.wall_parameters.thickness / 2,
                self.hot_swap_parameters.body_thickness / 2,
            ]
        )

    def led_placement_top(self) -> Manifold:
        clearance = self.hot_swap_parameters.mask_clearance
        h = self.led.pcb_height + clearance + 3.8
        return self.centralize_led_object(
            Manifold.cube(
                [
                    self.switches_parameters.size,
                    self.switches_parameters.size,
                    h,
                ],
                center=True,
            )
        ).translate(
            [
                0,
                0,
                self.hot_swap_parameters.body_thickness
                + clearance
                - h / 2
                - 0.1,
            ]
        )

    def centralize_led_object(self, obj: Manifold) -> Manifold:
        return obj.translate(
            [
                0,
                -self.hot_swap_parameters.cube_size / 2 + self.led.led_size / 2,
                0,
            ]
        )

    def switch_socket(self) -> Manifold:
        clearance = self.hot_swap_parameters.mask_clearance
        body_holder = Manifold.cube(
            [
                self.switches_parameters.size,
                self.switches_parameters.size,
                self.hot_swap_parameters.switch_socket_height + clearance,
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
                    self.hot_swap_parameters.switch_socket_width + clearance,
                    self.switches_parameters.size,
                    self.hot_swap_parameters.switch_socket_height + clearance,
                ],
                center=True,
            )
            + body_holder
        )
        return cube.translate(
            [0, 0, self.hot_swap_parameters.switch_socket_height / 2]
        )

    def assemble(self) -> Manifold:
        return self.body() + self.led_placement_top() + self.switch_socket()


if __name__ == "__main__":
    mask = injector.get(HotSwapPlacementMaskCAD)
    mask.program(sys.argv)
