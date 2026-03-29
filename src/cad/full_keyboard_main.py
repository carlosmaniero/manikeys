from __future__ import annotations
from context import injector
import sys
import openscad as osc
from dataclasses import dataclass
from models.body import BodyModel
from models.parameters import Parameters
from injector import inject, singleton
from loader import load_stl
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class FullKeyboardMain(OSCObject):
    model: BodyModel
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        divider_y = self.model.divider_y

        height = self.model.sphere.highest + self.parameters.body.height

        mask = (
            osc.cube(
                [
                    self.model.width,
                    self.model.end_y() - divider_y,
                    height * 2,
                ],
            )
            .right(self.model.start_x())
            .back(divider_y)
            .down(self.parameters.body.height)
        )

        body = load_stl("build/full_keyboard.stl")

        return body & mask


if __name__ == "__main__":
    full_keyboard_main = injector.get(FullKeyboardMain)
    full_keyboard_main.program(sys.argv)
