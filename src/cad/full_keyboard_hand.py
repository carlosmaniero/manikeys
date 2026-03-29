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
class FullKeyboardHand(OSCObject):
    model: BodyModel
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        divider_y = self.model.divider_y

        height = self.model.sphere.highest + self.parameters.body.height

        # Everything where y < divider_y AND x > hand_support_end_x
        mask = (
            osc.cube(
                [
                    self.model.end_x() - self.model.hand_support_end_x,
                    divider_y - self.model.start_y(),
                    height * 2,
                ],
            )
            .right(self.model.hand_support_end_x)
            .back(self.model.start_y())
            .down(self.parameters.body.height)
        )

        body = load_stl("build/full_keyboard.stl")

        return body & mask


if __name__ == "__main__":
    full_keyboard_hand = injector.get(FullKeyboardHand)
    full_keyboard_hand.program(sys.argv)
