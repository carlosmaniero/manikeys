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
class SocketGrid(OSCObject):
    layout: Layout
    cad_thump: CapThumbModel

    def assemble(self):
        grid = []
        cap = load_stl("build/cad/socket_adapter.stl").rotx(180)

        offset = [0, 0, -2]

        cap += offset

        for column in self.layout.grid:
            for key in column:
                grid.append(cap.rotate(key.rotation) + key.position)

        for position in self.cad_thump.get_positions():
            grid.append(cap + position)

        return osc.union(*grid)


if __name__ == "__main__":
    grid = injector.get(SocketGrid)
    grid.program(sys.argv)
