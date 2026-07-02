from __future__ import annotations
from globals.wall.parameters import WallParameters
from structure.body.parameters import BodyParameters
from core.context import injector
import sys
import manifold3d
from dataclasses import dataclass
from structure.body.models import BodyInnerModel, BodyModel
from injector import inject, singleton
from core.loader import load_stl_to_manifold
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class BodyInnerSections(ManifoldObject):
    model: BodyInnerModel
    body: BodyModel
    wall_parameters: WallParameters
    body_parameters: BodyParameters

    def assemble(self) -> manifold3d.Manifold:
        divider_size = self.wall_parameters.thickness * 2
        divider_y = self.model.divider_y - divider_size / 2

        divider = manifold3d.Manifold.cube(
            [
                self.model.width,
                divider_size,
                self.model.sphere.highest + self.body_parameters.height,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                divider_y,
                -self.body_parameters.height,
            ]
        )

        height = self.model.sphere.highest + self.body_parameters.height

        side_mask = manifold3d.Manifold.cube(
            [
                self.body.hand_support_end_x
                - self.body.start_x()
                + self.wall_parameters.thickness,
                self.body.divider_y - self.body.start_y(),
                height * 2,
            ],
            center=False,
        ).translate(
            [
                self.body.start_x(),
                self.body.start_y(),
                -self.body_parameters.height,
            ]
        )

        body = (
            load_stl_to_manifold("build/structure/body/cad/body_cavity.stl")
            - side_mask
        )

        return body - divider


if __name__ == "__main__":
    bodyInnerSections = injector.get(BodyInnerSections)
    bodyInnerSections.program(sys.argv)
