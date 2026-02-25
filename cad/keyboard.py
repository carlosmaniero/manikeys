from dataclasses import dataclass
import openscad as osc
from injector import inject
from models.projection import SphereProjection
from models.parameters import Parameters
from .cap import CapCAD


@inject
@dataclass
class KeyboardCAD:
    projection: SphereProjection
    parameters: Parameters
    cap_cad: CapCAD

    def body_mask(self):
        p = self.parameters
        center = [
            p.body.width / 2,
            p.body.depth / 2,
            p.body.thickness,
        ]

        [position, rotation] = self.projection.project_with_rotation(center)

        obj = osc.cube(
            [
                p.body.width,
                p.body.depth,
                p.body.radius,
            ],
            center=True,
        )

        obj += [0, 0, p.body.thickness / 2]
        obj = osc.color(obj, "red")

        obj = obj.rotate(rotation)
        obj = obj.translate(position)

        return obj

    def body(self):
        p = self.parameters
        obj = osc.sphere(p.body.radius)
        obj += [0, 0, p.body.radius - p.body.thickness]

        internal_radius = p.body.radius
        obj -= osc.sphere(internal_radius) + [0, 0, p.body.radius]

        return obj.intersection(self.body_mask())

    def assembly(self):
        return self.cap_cad.assembly_grid()
