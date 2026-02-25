from dataclasses import dataclass, field
import openscad as osc
from injector import inject
from models.layout import Layout
from models.parameters import Parameters


@inject
@dataclass
class CapCAD:
    layout: Layout
    parameters: Parameters
    fn: int = field(default=20, init=False)

    def outer(self):
        p = self.parameters
        obj = osc.cube(
            [
                p.caps.size + p.caps.border * 2,
                p.caps.size + p.caps.border * 2,
                p.caps.outer.thickness,
            ],
            center=True,
        )

        obj += [0, 0, p.caps.outer.thickness / 2]
        obj = osc.color(obj, "blue")
        obj = obj.fillet(p.caps.border / 4, fn=self.fn)

        return obj

    def cap(self):
        p = self.parameters
        body = self.outer()

        obj = osc.cube(
            [
                p.caps.size,
                p.caps.size,
                p.caps.thickness + p.globals.diff_offset,
            ],
            center=True,
        )

        obj += [0, 0, p.caps.thickness / 2]
        obj = osc.color(obj, "red")

        return body - obj

    def assembly_grid(self):
        grid = []

        for column in self.layout.grid:
            for key in column:
                grid.append(self.cap().rotate(key.rotation) + key.position)

        return osc.union(*grid)
