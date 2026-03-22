import sys
from dataclasses import dataclass
import openscad as osc
from injector import inject, singleton
from models.layout import Layout
from models.cap_thumb import CapThumbModel
from openscad_ext.object import OSCObject
from context import injector
from loader import load_stl


@singleton
@inject
@dataclass
class CapTopGridCAD(OSCObject):
    layout: Layout
    cad_thump: CapThumbModel

    def assemble(self):
        grid = []
        cap = load_stl("dist/Simple-CherryMX-Keycap.stl")

        offset = [3, -1.25, 4]

        for column in self.layout.grid:
            for key in column:
                grid.append(cap.rotate(key.rotation) + key.position + offset)

        for position in self.cad_thump.get_positions():
            grid.append(cap + position + offset)

        return osc.union(*grid)


if __name__ == "__main__":
    cap_grid = injector.get(CapTopGridCAD)
    cap_grid.program(sys.argv)
