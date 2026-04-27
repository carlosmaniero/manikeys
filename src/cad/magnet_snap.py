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
class MagnetSnapCAD(ManifoldObject):
    model: MagnetSnapModel
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        radius = (
            self.parameters.magnet.diameter
            + self.parameters.magnet.error_margin
        ) / 2
        height = self.model.full_magnet_height

        magnet = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            circular_segments=64,
            center=True,
        ).rotate([90, 0, 0])

        positions = self.model.get_all_positions()

        result = magnet.translate(positions[0])
        for pos in positions[1:]:
            result += magnet.translate(pos)

        return result


if __name__ == "__main__":
    magnet_snap = injector.get(MagnetSnapCAD)
    magnet_snap.program(sys.argv)
