from __future__ import annotations
from context import injector
import sys
import manifold3d
from dataclasses import dataclass
from models.body import BodyInnerModel, BodyModel
from models.parameters import Parameters
from injector import inject, singleton
from loader import load_stl_to_manifold
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class BodyInnerSections(ManifoldObject):
    model: BodyInnerModel
    body: BodyModel
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        divider_size = self.parameters.body.thickness * 2
        divider_y = self.model.divider_y - divider_size / 2

        divider = manifold3d.Manifold.cube(
            [
                self.model.width,
                divider_size,
                self.model.sphere.highest + self.parameters.body.height,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                divider_y,
                -self.parameters.body.height,
            ]
        )

        height = self.model.sphere.highest + self.parameters.body.height

        side_mask = manifold3d.Manifold.cube(
            [
                self.body.hand_support_end_x
                - self.body.start_x()
                + self.parameters.body.thickness,
                self.body.divider_y - self.body.start_y(),
                height * 2,
            ],
            center=False,
        ).translate(
            [
                self.body.start_x(),
                self.body.start_y(),
                -self.parameters.body.height,
            ]
        )

        body = load_stl_to_manifold("build/cad/body_inner.stl") - side_mask

        return body - divider


if __name__ == "__main__":
    bodyInnerSections = injector.get(BodyInnerSections)
    bodyInnerSections.program(sys.argv)
