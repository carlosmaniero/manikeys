import sys
from dataclasses import dataclass

import openscad as osc
from injector import inject, singleton

from context import injector
from loader import load_stl
from models.cap_thumb import CapThumbModel
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class CapThumbHoleCAD(OSCObject):
    model: CapThumbModel

    def assemble(self):
        hole = load_stl("build/cad/cap_hole.stl")
        positions = self.model.get_positions()

        holes = [hole + pos for pos in positions]

        return osc.color(osc.union(*holes), "orange")


if __name__ == "__main__":
    cap_thumb_hole = injector.get(CapThumbHoleCAD)
    cap_thumb_hole.program(sys.argv)
