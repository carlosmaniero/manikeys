from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl
from models.body import BodyModel
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class RenderCAD(OSCObject):
    model: BodyModel

    def assemble(self) -> osc.PyOpenSCAD:
        left = load_stl("build/main.3mf")

        right = osc.mirror(left, [1, 0, 0])

        distance = self.model.end_x() + 200
        right = osc.translate(right, [distance, 0, 0])

        return left | right


if __name__ == "__main__":
    render = injector.get(RenderCAD)
    render.program(sys.argv)
