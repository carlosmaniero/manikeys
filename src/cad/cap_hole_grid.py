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
class CapHoleGridCAD(OSCObject):
    layout: Layout

    def assemble(self):
        holes = []

        for column in self.layout.grid:
            for key in column:
                hole = load_stl("build/cad/cap_hole.stl")
                hole = hole.rotate(key.rotation) + key.position
                holes.append(hole)

        return osc.color(osc.union(*holes), "orange")


if __name__ == "__main__":
    cap_hole_grid = injector.get(CapHoleGridCAD)
    cap_hole_grid.program(sys.argv)
