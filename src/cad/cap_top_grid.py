import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from models.layout import Layout
from models.cap_thumb import CapThumbModel
from manifold_ext.object import ManifoldObject
from context import injector
from loader import load_stl_to_manifold
import os

DEBUG = os.getenv("DEBUG", "false") == "true"


@singleton
@inject
@dataclass
class CapTopGridCAD(ManifoldObject):
    layout: Layout
    cad_thump: CapThumbModel

    def show(self):
        if DEBUG:
            try:
                # We can't easily show both in ManifoldObject.show() yet
                # because it's a simple implementation.
                # For now, let's just assemble and show the grid.
                pass
            except Exception as e:
                print("build the body to use debugging", e)

        return super().show()

    def assemble(self) -> manifold3d.Manifold:
        grid = []
        cap = load_stl_to_manifold("dist/Simple-CherryMX-Keycap.stl")

        offset = [3, -1.25, 4]

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    cap.rotate(key.rotation)
                    .translate(key.position)
                    .translate(offset)
                )

        for position in self.cad_thump.get_positions():
            grid.append(cap.translate(position).translate(offset))

        return manifold3d.Manifold.batch_boolean(grid, manifold3d.OpType.Add)


if __name__ == "__main__":
    cap_grid = injector.get(CapTopGridCAD)
    cap_grid.program(sys.argv)
