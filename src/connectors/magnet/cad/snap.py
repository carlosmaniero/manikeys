from __future__ import annotations
from connectors.magnet.parameters import MagnetParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from connectors.magnet.models import MagnetSnapModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MagnetSnapCAD(ManifoldObject):
    model: MagnetSnapModel
    magnet_parameters: MagnetParameters

    def assemble(self) -> manifold3d.Manifold:
        radius = (
            self.magnet_parameters.diameter
            + self.magnet_parameters.error_margin
        ) / 2
        height = self.model.full_magnet_height

        magnet_y = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            circular_segments=64,
            center=True,
        ).rotate([90, 0, 0])

        magnet_x = manifold3d.Manifold.cylinder(
            radius_low=radius,
            radius_high=radius,
            height=height,
            circular_segments=64,
            center=True,
        ).rotate([0, 90, 0])

        result = manifold3d.Manifold()

        for pos in self.model.get_y_axis_positions():
            m = magnet_y.translate(pos)
            result += m

        for pos in self.model.get_x_axis_positions():
            m = magnet_x.translate(pos)
            result += m

        return result


if __name__ == "__main__":
    magnet_snap = injector.get(MagnetSnapCAD)
    magnet_snap.program(sys.argv)
