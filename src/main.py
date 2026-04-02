from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class Keyboard(OSCObject):
    def assemble(self) -> osc.PyOpenSCAD:
        body = load_stl("build/full_keyboard.stl")
        body |= load_stl("build/cad/body_bottom.stl")
        body |= load_stl("build/cad/socket_adapter_grid.stl")
        body = osc.color(body, "#c0b89b")

        body |= osc.color(load_stl("build/cad/cap_top_grid.stl"), "#bec0b1")

        return body


if __name__ == "__main__":
    keyboard = injector.get(Keyboard)
    keyboard.program(sys.argv)
