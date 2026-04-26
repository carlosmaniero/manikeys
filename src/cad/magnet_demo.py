from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.magnet_snap import MagnetSnapModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MagnetDemoCAD(ManifoldObject):
    model: MagnetSnapModel
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        # Hole dimensions matching the actual snap holes
        radius = (
            self.parameters.magnet.diameter
            + self.parameters.magnet.error_margin
        ) / 2
        hole_depth = self.model.full_magnet_height

        # Test block dimensions
        block_size = self.parameters.magnet.diameter + 6.0
        block_height = 3.0  # The entire object must have 3mm height

        block = manifold3d.Manifold.cube(
            [block_size, block_size, block_height],
            center=True,
        )

        # Hole to match the snap holes
        hole = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=hole_depth + 0.1,  # slightly taller for clean cut
            circular_segments=64,
            center=True,
        ).translate([0, 0, block_height / 2 - hole_depth / 2])

        return block - hole


if __name__ == "__main__":
    demo = injector.get(MagnetDemoCAD)
    demo.program(sys.argv)
