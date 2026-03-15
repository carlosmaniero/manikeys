import sys
from dataclasses import dataclass, field
import openscad as osc
from injector import inject, singleton
from models.parameters import Parameters
from openscad_ext.object import OSCObject
from context import injector


@singleton
@inject
@dataclass
class CapCAD(OSCObject):
    parameters: Parameters
    fn: int = field(default=20, init=False)

    def assemble(self):
        p = self.parameters

        squared_bottom = osc.cube(
            [
                p.caps.size + p.caps.border * 2,
                p.caps.size + p.caps.border * 2,
                p.caps.thickness / 2,
            ],
            center=True,
        )

        squared_bottom += [0, 0, -p.caps.thickness / 4]

        obj = osc.cube(
            [
                p.caps.size + p.caps.border * 2,
                p.caps.size + p.caps.border * 2,
                p.caps.thickness,
            ],
            center=True,
        )
        obj = obj.fillet(p.caps.border / 4, fn=self.fn)

        obj |= squared_bottom

        obj -= [0, 0, p.caps.thickness / 2 - p.caps.outer.thickness]

        return self.colorize(obj)

    def colorize(self, obj):
        return osc.color(obj, "orange")


if __name__ == "__main__":
    cap = injector.get(CapCAD)
    cap.program(sys.argv)
