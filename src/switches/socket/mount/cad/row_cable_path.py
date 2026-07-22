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
        row_pins = len(self.model.layout.grid)
        row_header = load_stl_to_manifold(
            f"build/components/female_pin_header/cad/female_pin_header_body_{row_pins}.stl"
        )
        return row_header.rotate([0, 180, 180]).translate(
            self.model.pin_header_position
        )


if __name__ == "__main__":
    cable_path = injector.get(RowCablePathCAD)
    cable_path.program(sys.argv)
