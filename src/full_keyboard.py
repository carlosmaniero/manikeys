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
class FullKeyboard(OSCObject):
    def assemble(self) -> osc.PyOpenSCAD:
        body = load_stl("build/cad/body.stl")
        body -= load_stl("build/cad/body_inner_sections.stl")
        body |= load_stl("build/cad/cap_grid.stl")
        body -= load_stl("build/cad/cap_hole_grid.stl")
        body |= load_stl("build/cad/cap_thumb.stl")
        body -= load_stl("build/cad/cap_thumb_hole.stl")

        return body


if __name__ == "__main__":
    full_keyboard = injector.get(FullKeyboard)
    full_keyboard.program(sys.argv)
