from __future__ import annotations
from globals.wall.parameters import WallParameters
import sys
import numpy as np
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class LogoCAD(ManifoldObject):
    body: BodyModel
    wall_parameters: WallParameters

    def assemble(self) -> manifold3d.Manifold:
        logo = load_stl_to_manifold("dist/mani-logo.stl")

        logo_w = 15.00
        logo_d = 44.431

        x_start = self.body.divider_x_main
        x_end = self.body.end_x() - self.wall_parameters.fillet / 2
        center_x = (x_start + x_end) / 2

        target_x = center_x - logo_w / 2
        target_y = (
            self.body.end_y()
            - self.wall_parameters.fillet
            - self.wall_parameters.thickness
            - logo_d
        )
        center_y = target_y + logo_d / 2

        target_z = (
            float(self.body.z(np.array([center_x]), np.array([center_y]))[0])
            - 2
        )

        return logo.translate([target_x, target_y, target_z])


if __name__ == "__main__":
    logo = injector.get(LogoCAD)
    logo.program(sys.argv)
