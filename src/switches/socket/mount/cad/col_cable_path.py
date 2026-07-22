from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from globals.wall.parameters import WallParameters
from switches.socket.mount.models import ColCablePathModel


from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class ColCablePathCAD(ManifoldObject):
    model: ColCablePathModel
    wall_parameters: WallParameters

    def assemble(self) -> manifold3d.Manifold:
        cable_hook = load_stl_to_manifold(
            "build/components/cable_hook/cad/cable_hook.stl"
        )
        result = manifold3d.Manifold()

        for x, y, z_min, height in self.model.path:
            result += cable_hook.scale([1.0, 1.0, height]).translate(
                [x, y, z_min]
            )

        col_pins = len(self.model.layout.grid[len(self.model.layout.grid) - 1])
        col_header = load_stl_to_manifold(
            f"build/components/female_pin_header/cad/female_pin_header_lid_{col_pins}.stl"
        )
        result += col_header.rotate([0, 180, 90]).translate(
            self.model.pin_header_position
        )

        return result


if __name__ == "__main__":
    cable_path = injector.get(ColCablePathCAD)
    cable_path.program(sys.argv)
