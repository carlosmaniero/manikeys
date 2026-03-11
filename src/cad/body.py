from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.body import BodyModel
from openscad_ext.loft import loft, Profile
from cad.cap import CapCAD
import openscad as osc
import os

"""
The body is created using a loft that is then rotated [90, 0, 90].
To make the math intuitive, we use the final coordinate system:
- x axis: left to right (width)  => Loft extrusion axis
- y axis: front to back (depth)  => Profile horizontal axis
- z axis: up to down (height)    => Profile vertical axis
"""

SLICES = int(os.getenv("SLICES", 800))


@singleton
@inject
@dataclass
class BodyProfile:
    model: BodyModel

    def __call__(self, x: float) -> Profile:
        return Profile(
            upper=lambda y: self.model.top_z(x, y),
            lower=lambda y: -self.model.parameters.body.height - 10,
            span=(
                self.model.start_y(),
                self.model.end_y(),
            ),
            segments=SLICES,
            breakpoints=[self.model.fillet_end_y],
        )


@singleton
@inject
@dataclass
class BodyCAD:
    cap_cad: CapCAD
    model: BodyModel
    profile: BodyProfile

    def assembly(self):
        return loft(
            self.profile,
            span=(self.model.start_x(), self.model.end_x()),
            breakpoints=[self.model.fillet_start_x],
            slices=SLICES,
            fn=SLICES,
        ).rotate([90, 0, 90])

    @property
    def filename(self) -> str:
        return "build/body.3mf"

    def export(self):
        body_cad = self.assembly()
        body_cad.export(self.filename)


if __name__ == "__main__":
    body = injector.get(BodyCAD)
    body_cad = body.assembly()
    body_cad = osc.color(body_cad, "#333333")
    body_cad.show()
