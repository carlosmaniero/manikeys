from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from globals.wall.parameters import WallParameters
from switches.socket.mount.models import RowCablePathModel
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class RowCablePathCAD(ManifoldObject):
    model: RowCablePathModel
    wall_parameters: WallParameters

    def assemble(self) -> manifold3d.Manifold:
        cable_hook = load_stl_to_manifold(
            "build/components/cable_hook/cad/cable_hook.stl"
        )
        result = manifold3d.Manifold()

        for x, y, z_min, height in self.model.path:
            result += (
                cable_hook.scale([1.0, 1.0, height])
                .rotate([0, 0, -90])
                .translate([x, y, z_min])
            )

        return result


if __name__ == "__main__":
    cable_path = injector.get(RowCablePathCAD)
    cable_path.program(sys.argv)
