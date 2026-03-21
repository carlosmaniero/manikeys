import sys
from dataclasses import dataclass
import openscad as osc
from injector import inject, singleton
from models.parameters import Parameters
from openscad_ext.object import OSCObject
from context import injector


@singleton
@inject
@dataclass
class CapHoleCAD(OSCObject):
    parameters: Parameters

    def assemble(self):
        return osc.cube(
            [
                self.parameters.caps.size,
                self.parameters.caps.size,
                self.parameters.caps.thickness * 5
                + self.parameters.globals.diff_offset * 2,
            ],
            center=True,
        )


if __name__ == "__main__":
    cap_hole = injector.get(CapHoleCAD)
    cap_hole.program(sys.argv)
