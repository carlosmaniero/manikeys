from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.rj11 import RJ11Model
from models.body import BodyModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class PlacementMaskCAD(ManifoldObject):
    parameters: Parameters
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
        return (
            self.model.rj11.width
            + self.parameters.body.thickness * 4
            + self.tab_width * 2
            + self.parameters.body.fillet
        )

    @property
    def tab_width(self) -> float:
        return (
            self.parameters.body.m2_screw_diameter
            + self.parameters.body.thickness * 2
        )

    @property
    def total_height(self) -> float:
        return (
            self.model.rj11.height
            + self.parameters.body.thickness
            + self.height
        )

    @property
    def main_block(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.width,
                self.model.rj11.length + self.parameters.body.thickness,
                self.total_height + self.body_model.highest,
            ],
            center=True,
        ).translate([0, 0, self.body_model.highest / 2])

    def assemble(self) -> manifold3d.Manifold:
        max_y = self.model.rj11.length / 2 + self.parameters.body.thickness

        return self.main_block.translate(
            [
                self.body_model.end_x() - self.width / 2,
                self.body_model.end_y() - max_y,
                self.body_model.bottom_z + self.total_height / 2,
            ]
        )


if __name__ == "__main__":
    mask = injector.get(PlacementMaskCAD)
    mask.program(sys.argv)
