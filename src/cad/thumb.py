from dataclasses import dataclass
from injector import inject
from models.parameters import Parameters
import openscad as osc


@inject
@dataclass
class ThumbCAD:
    parameters: Parameters

    def mask(self):
        depth = (self.parameters.caps.size + self.parameters.caps.gap) * 2
        width = (self.parameters.caps.size + self.parameters.caps.gap) * 3

        body = osc.cube(
            [
                width,
                depth * 2 + self.parameters.body.fillet,
                self.parameters.body.height + self.parameters.body.fillet / 2,
            ],
        )
        body -= [
            0,
            depth * 2 - self.parameters.body.fillet * 2,
            self.parameters.body.height + self.parameters.body.fillet,
        ]

        return self.transformation(body)

    def transformation(self, obj):
        obj = obj.fillet(self.parameters.body.fillet / 2, fn=100)

        obj += [0, 0, self.parameters.body.fillet]

        obj = obj.rotate([0, 0, -25])

        return obj

    def assembly(self):
        depth = (self.parameters.caps.size + self.parameters.caps.gap) * 2
        width = (self.parameters.caps.size + self.parameters.caps.gap) * 3

        points = [
            [self.parameters.body.fillet - 3, -self.parameters.body.fillet],
            [
                self.parameters.body.height + self.parameters.body.fillet,
                -self.parameters.body.fillet,
            ],
            [
                self.parameters.body.height + self.parameters.body.fillet,
                depth + self.parameters.body.fillet,
            ],
            [
                self.parameters.body.height,
                depth + self.parameters.body.fillet,
            ],
        ]

        shape = osc.polygon(points)
        shape = shape.rotate([0, 90, 180])

        shape += [
            width,
            0,
            0,
        ]

        body = shape.linear_extrude(width)

        return self.transformation(body)
