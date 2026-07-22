from __future__ import annotations
import manifold3d
from dataclasses import dataclass
from core.manifold_ext.object import ManifoldObject
from components.female_pin_header.model import FemalePinHeaderModel


@dataclass
class FemalePinHeaderBodyBaseCAD(ManifoldObject):
    model: FemalePinHeaderModel

    def create_housing(self, pins: int) -> manifold3d.Manifold:
        outer = manifold3d.Manifold.cube(
            [
                self.model.outer_length(pins),
                self.model.outer_width,
                self.model.outer_height,
            ],
            center=True,
        )

        inner_pocket = manifold3d.Manifold.cube(
            [
                self.model.inner_length(pins),
                self.model.inner_width,
                self.model.inner_height + 0.1,
            ],
            center=True,
        ).translate([0.0, 0.0, self.model.parameters.wall_thickness / 2 + 0.05])

        wire_hole = manifold3d.Manifold.cube(
            [
                self.model.wire_hole_length(pins),
                self.model.wire_hole_width,
                self.model.parameters.wall_thickness + 0.2,
            ],
            center=True,
        ).translate(
            [
                0.0,
                0.0,
                -self.model.outer_height / 2
                + self.model.parameters.wall_thickness / 2
                - 0.1,
            ]
        )

        housing = outer - inner_pocket - wire_hole

        cut_box = manifold3d.Manifold.cube(
            [
                self.model.outer_length(pins) + 2.0,
                self.model.outer_width,
                self.model.outer_height + 2.0,
            ],
            center=True,
        ).translate([0.0, self.model.outer_width / 2, 0.0])

        half_body = housing ^ cut_box

        extra_width = 3.0
        extra_structure = manifold3d.Manifold.cube(
            [
                self.model.outer_length(pins),
                extra_width,
                self.model.outer_height,
            ],
            center=True,
        ).translate([0.0, self.model.outer_width / 2 + extra_width / 2, 0.0])

        holes = manifold3d.Manifold()
        hole_radius = 0.6
        for col in range(pins):
            x = (col - (pins - 1) / 2) * self.model.parameters.pitch
            hole = manifold3d.Manifold.cube(
                [1.2, 1.2, self.model.outer_height + 0.2],
                center=True,
            ).translate([x, self.model.outer_width / 2 + extra_width / 2, 0.0])
            holes += hole

        return half_body + (extra_structure - holes)
