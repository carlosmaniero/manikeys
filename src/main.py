from __future__ import annotations
import sys
import openscad as osc
from injector import inject, singleton
from context import injector
from cad.cap import CapCAD
from loader import load_stl
from openscad_ext.object import OSCObject


@singleton
@inject
class Keyboard(OSCObject):
    def __init__(self, cap_cad: CapCAD):
        self.cap_cad = cap_cad

    def assemble(self) -> osc.PyOpenSCAD:
        body = load_stl("build/cad/body.stl")
        body |= self.cap_cad.assembly_grid()
        body -= self.cap_cad.cap_holes()
        return body


if __name__ == "__main__":
    keyboard = injector.get(Keyboard)
    keyboard.program(sys.argv)
