from __future__ import annotations
import sys
import openscad as osc
from typing import Iterator
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_many_stl
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class Keyboard(OSCObject):
    def assemble(self) -> Iterator[osc.PyOpenSCAD]:
        paths = [
            "build/full_keyboard.stl",
            "build/cad/body_bottom.stl",
            "build/cad/socket_adapter_grid.stl",
            "build/cad/cap_top_grid.stl",
        ]
        body_part, bottom, sockets, caps = load_many_stl(paths)

        yield body_part.color("#c0b89b")
        yield bottom.color("#c0b89b")
        yield sockets.color("#c0b89b")
        yield caps.color("#bec0b1")


if __name__ == "__main__":
    keyboard = injector.get(Keyboard)
    keyboard.program(sys.argv)
