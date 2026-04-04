from __future__ import annotations
from context import injector
import sys
import manifold3d
from dataclasses import dataclass
from models.socket_placement import SocketPlacementInner
from models.parameters import Parameters
from injector import inject, singleton
from loader import load_stl_to_manifold
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class SocketPlacementInnerSections(ManifoldObject):
    model: SocketPlacementInner
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        divider_size = (
            self.parameters.body.thickness * 4
            + self.parameters.body.clearance * 2
        )
        divider_y = self.model.divider_y - divider_size / 2

        height = self.model.sphere.highest + self.parameters.body.height

        divider = manifold3d.Manifold.cube(
            [
                self.model.width,
                divider_size,
                height,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                divider_y,
                -self.parameters.body.height,
            ]
        )

        side_section = manifold3d.Manifold.cube(
            [
                self.model.hand_support_end_x - self.model.hand_support_start_x,
                divider_y - self.model.start_y(),
                height,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                self.model.start_y(),
                -self.parameters.body.height,
            ]
        )

        body = load_stl_to_manifold("build/cad/socket_placement_inner.stl")

        return body - (divider + side_section)


if __name__ == "__main__":
    socketPlacementInnerSections = injector.get(SocketPlacementInnerSections)
    socketPlacementInnerSections.program(sys.argv)
