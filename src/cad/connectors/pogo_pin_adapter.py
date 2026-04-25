from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.parameters import Parameters
from models.pogo_pin import PogoPinModel
from models.body import BodyModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class PogoPinAdapterCAD(ManifoldObject):
    parameters: Parameters
    model: PogoPinModel
    body_model: BodyModel

    @property
    def main_block(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.model.adapter_width,
                self.model.adapter_length,
                self.model.adapter_height,
            ],
            center=True,
        ).translate(
            [
                0,
                0,
                self.model.adapter_z_center,
            ]
        )

    @property
    def internal_mask(self) -> manifold3d.Manifold:
        return load_stl_to_manifold("build/cad/connectors/pogo_pin_mask.stl")

    @property
    def screw_holes(self) -> manifold3d.Manifold:
        radius = self.model.adapter_screw_hole_diameter / 2
        height = self.model.thickness + 5.0
        distance = self.model.mounting_hole_distance

        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            circular_segments=60,
            center=True,
        )

        return (
            hole.translate([distance / 2, 0, 0])
            + hole.translate([-distance / 2, 0, 0])
        ).translate([0, 0, self.model.flange_z_offset])

    def assemble(self) -> manifold3d.Manifold:
        return self.main_block - self.internal_mask - self.screw_holes


if __name__ == "__main__":
    adapter = injector.get(PogoPinAdapterCAD)
    adapter.program(sys.argv)
