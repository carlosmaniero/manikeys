import sys
from dataclasses import dataclass, field
import openscad as osc
from injector import inject, singleton
from models.parameters import Parameters
from core.openscad_ext.object import OSCObject
from core.context import injector


@singleton
@inject
@dataclass
class SwitchHoleDecoratorCAD(OSCObject):
    parameters: Parameters
    fn: int = field(default=20, init=False)

    def assemble(self):
        p = self.parameters

        squared_bottom = osc.cube(
            [
                p.switches.size + p.switches.border * 2,
                p.switches.size + p.switches.border * 2,
                p.switches.thickness / 2,
            ],
            center=True,
        )

        squared_bottom += [0, 0, -p.switches.thickness / 4]

        obj = osc.cube(
            [
                p.switches.size + p.switches.border * 2,
                p.switches.size + p.switches.border * 2,
                p.switches.thickness,
            ],
            center=True,
        )
        obj = obj.fillet(p.switches.border / 4, fn=self.fn)

        obj |= squared_bottom

        obj -= [0, 0, p.switches.thickness / 2 - p.switches.outer.thickness]

        return self.colorize(obj)

    def colorize(self, obj):
        return osc.color(obj, "orange")


if __name__ == "__main__":
    switch_hole_decorator = injector.get(SwitchHoleDecoratorCAD)
    switch_hole_decorator.program(sys.argv)
