import sys
from dataclasses import dataclass
import openscad as osc
from injector import inject, singleton
from models.layout import Layout
from openscad_ext.object import OSCObject
from context import injector
from loader import load_stl


@singleton
@inject
@dataclass
class CapTopGridCAD(OSCObject):
    layout: Layout

    def assemble(self):
        grid = []
        cap = load_stl("dist/Simple-CherryMX-Keycap.stl")

        for column in self.layout.grid:
            for key in column:
                grid.append(
                    (cap.rotate(key.rotation) + key.position) + [3, 0, 4]
                )

        return osc.union(*grid)


if __name__ == "__main__":
    cap_grid = injector.get(CapTopGridCAD)
    cap_grid.program(sys.argv)
