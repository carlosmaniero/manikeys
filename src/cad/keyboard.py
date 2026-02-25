from dataclasses import dataclass
import openscad as osc
from injector import inject
from models.projection import SphereProjection
from models.parameters import Parameters
from models.layout import Layout
from .cap import CapCAD


@inject
@dataclass
class KeyboardCAD:
    projection: SphereProjection
    parameters: Parameters
    cap_cad: CapCAD
    layout: Layout

    def cap_body_mask(self):
        return osc.cube(
            [
                self.parameters.caps.size + self.parameters.caps.gap * 2,
                self.parameters.caps.size + self.parameters.caps.gap * 2,
                self.parameters.body.thickness * 2
                + self.parameters.globals.diff_offset,
            ],
            center=True,
        )

    def body_mask(self):
        masks = []

        for column in self.layout.grid:
            for key in column:
                mask = self.cap_body_mask()
                mask = mask.rotate(key.rotation) + key.position
                masks.append(mask)

        return osc.union(*masks)

    def body(self):
        p = self.parameters
        obj = osc.sphere(p.body.radius)
        obj += [0, 0, p.body.radius - p.body.thickness]

        internal_radius = p.body.radius
        obj -= osc.sphere(internal_radius) + [0, 0, p.body.radius]

        return self.colorize(obj.intersection(self.body_mask()))

    def colorize(self, obj):
        return osc.color(obj, "#333333")

    def assembly(self):
        return (
            self.body() | self.cap_cad.assembly_grid()
        ) - self.cap_cad.cap_holes()
