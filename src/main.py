from __future__ import annotations
import sys
import openscad as osc
from injector import inject, singleton
from context import injector
from loader import load_stl
from openscad_ext.object import OSCObject


@singleton
@inject
class Keyboard(OSCObject):
    def __init__(self):
        pass

    def assemble(self) -> osc.PyOpenSCAD:
        body = load_stl("build/cad/body.stl")
        body -= load_stl("build/cad/body_inner.stl")
        body |= load_stl("build/cad/cap_grid.stl")
        body -= load_stl("build/cad/cap_hole_grid.stl")
        return body


if __name__ == "__main__":
    keyboard = injector.get(Keyboard)
    keyboard.program(sys.argv)
