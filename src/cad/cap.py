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

    def cap(self):
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

    def cap_body_mask_hole(self):
        return osc.cube(
            [
                self.parameters.caps.size,
                self.parameters.caps.size,
                self.parameters.caps.thickness * 2
                + self.parameters.globals.diff_offset * 2,
            ],
            center=True,
        )

    def cap_holes(self):
        holes = []

        for column in self.layout.grid:
            for key in column:
                hole = self.cap_body_mask_hole()
                hole = hole.rotate(key.rotation) + key.position
                holes.append(hole)

        return self.colorize(osc.union(*holes))

    def colorize(self, obj):
        return osc.color(obj, "orange")

    def assembly_grid(self):
        grid = []

        for column in self.layout.grid:
            for key in column:
                grid.append(self.cap().rotate(key.rotation) + key.position)

        return osc.union(*grid)
