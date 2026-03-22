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
class CapThumbCAD(OSCObject):
    model: CapThumbModel

    def assemble(self):
        cap = load_stl("build/cad/cap.stl")
        positions = self.model.get_positions()

        caps = [cap + pos for pos in positions]

        return osc.union(*caps)


if __name__ == "__main__":
    cap_thumb = injector.get(CapThumbCAD)
    cap_thumb.program(sys.argv)
