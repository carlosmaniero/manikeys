import sys
from dataclasses import dataclass, field
import openscad as osc
from injector import inject, singleton
from models.parameters import SwitchesParameters
from core.openscad_ext.object import OSCObject
from core.context import injector


@singleton
@inject
@dataclass
class SwitchHoleDecoratorCAD(OSCObject):
    switches_parameters: SwitchesParameters
    fn: int = field(default=20, init=False)

    def assemble(self):
        p = self.switches_parameters

        squared_bottom = osc.cube(
            [
                p.size + p.border * 2,
                p.size + p.border * 2,
                p.thickness / 2,
            ],
            center=True,
        )

        squared_bottom += [0, 0, -p.thickness / 4]

        obj = osc.cube(
            [
                p.size + p.border * 2,
                p.size + p.border * 2,
                p.thickness,
            ],
            center=True,
        )
        obj = obj.fillet(p.border / 4, fn=self.fn)

        obj |= squared_bottom

        obj -= [0, 0, p.thickness / 2 - p.outer.thickness]

        return self.colorize(obj)

    def colorize(self, obj):
        return osc.color(obj, "orange")


if __name__ == "__main__":
    switch_hole_decorator = injector.get(SwitchHoleDecoratorCAD)
    switch_hole_decorator.program(sys.argv)
