from __future__ import annotations
from globals.wall.parameters import WallParameters
from globals.screw.parameters import ScrewParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from connectors.rj11.model import RJ11Model
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ11MaskCAD(ManifoldObject):
    wall_parameters: WallParameters
    screw_parameters: ScrewParameters
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
        return self.model.rj11.width + self.wall_parameters.thickness * 2

    @property
    def main_block(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.width + self.model.rj11.error_margin * 2,
                self.model.rj11.length + self.wall_parameters.thickness * 2,
                self.model.rj11.height
                + self.height
                + self.model.rj11.error_margin * 2,
            ],
            center=True,
        ).translate([0, 0, -self.height / 2])

    @property
    def tab_width(self) -> float:
        return (
            self.screw_parameters.m2_diameter
            + self.wall_parameters.thickness * 2
        )

    def assemble(self) -> manifold3d.Manifold:
        max_x = self.width / 2 + self.tab_width
        max_y = self.model.rj11.length / 2 + self.wall_parameters.thickness
        return self.main_block.translate(
            [
                self.body_model.end_x() - self.wall_parameters.fillet - max_x,
                self.body_model.end_y() - max_y,
                self.body_model.bottom_z
                + self.wall_parameters.thickness
                + self.model.rj11.height / 2
                + self.height,
            ]
        )


if __name__ == "__main__":
    mask = injector.get(RJ11MaskCAD)
    mask.program(sys.argv)
