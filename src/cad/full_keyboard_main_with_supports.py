from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.body import BodyModel
from models.parameters import Parameters
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class FullKeyboardMainWithSupports(ManifoldObject):
    model: BodyModel
    parameters: Parameters

    def _create_support(self, y_pos: float) -> manifold3d.Manifold:
        radius = self.parameters.body.thickness / 2
        width = self.model.width

        support = manifold3d.Manifold.cylinder(
            height=width,
            radius_low=radius,
            radius_high=radius,
            circular_segments=64,
            center=False,
        )

        support = support.rotate([0, 90, 0])

        x_start = self.model.start_x()
        z_pos = self.model.bottom_z + radius

        return support.translate([x_start, y_pos, z_pos])

    def _create_support_y(
        self, x_pos: float, angle: float
    ) -> manifold3d.Manifold:
        radius = self.parameters.body.thickness / 2
        depth = self.model.end_y() - self.model.divider_y + 20

        support = manifold3d.Manifold.cylinder(
            height=depth,
            radius_low=radius,
            radius_high=radius,
            circular_segments=64,
            center=False,
        )

        support = support.rotate([-90, 0, angle])

        z_pos = self.model.bottom_z + radius

        return support.translate([x_pos, self.model.divider_y, z_pos])

    def _create_mask(self) -> manifold3d.Manifold:
        divider_y = self.model.divider_y

        height = self.model.sphere.highest + self.parameters.body.height

        return manifold3d.Manifold.cube(
            [
                self.model.width,
                self.model.end_y() - divider_y,
                height * 2,
            ],
            center=False,
        ).translate(
            [
                self.model.start_x(),
                divider_y,
                -self.parameters.body.height,
            ]
        )

    def assemble(self) -> manifold3d.Manifold:
        body = load_stl_to_manifold("build/cad/full_keyboard_main.stl")
        inner = load_stl_to_manifold("build/cad/body_inner.stl")
        mask = self._create_mask()

        y_range = self.model.end_y() - self.model.divider_y

        center_x = self.model.start_x() + self.model.width / 2

        supports = (
            self._create_support(self.model.divider_y + y_range * 0.25)
            + self._create_support(self.model.divider_y + y_range * 0.375)
            + self._create_support(self.model.divider_y + y_range * 0.50)
            + self._create_support(self.model.divider_y + y_range * 0.625)
            + self._create_support(self.model.divider_y + y_range * 0.75)
            + self._create_support_y(center_x, 20)
            + self._create_support_y(center_x, -20)
            + self._create_support_y(center_x, 0)
        )

        support = supports ^ (inner ^ mask)

        return body + support


if __name__ == "__main__":
    main_with_supports = injector.get(FullKeyboardMainWithSupports)
    main_with_supports.program(sys.argv)
