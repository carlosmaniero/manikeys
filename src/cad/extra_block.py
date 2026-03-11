from dataclasses import dataclass
from injector import inject
from models.parameters import Parameters
from models.layout import Layout
import openscad as osc


@inject
@dataclass
class ExtraBlockCAD:
    parameters: Parameters
    layout: Layout

    def assembly(self):
        body = osc.cube(
            [
                70,
                self.layout.positioning.depth(),
                self.parameters.body.height
                + self.layout.positioning.right[2]
                + 30,
            ],
        )

        body = body.fillet(self.parameters.body.fillet, fn=100)

        body += self.layout.positioning.right
        body -= [
            0,
            0,
            self.layout.positioning.right[2] + self.parameters.body.height,
        ]

        return body
