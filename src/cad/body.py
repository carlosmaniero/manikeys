from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.body import BodyModel
from openscad_ext.loft import loft, Profile
from cad.cap import CapCAD
import openscad as osc

"""
The body is created using a loft that is then rotated [90, 0, 90].
To make the math intuitive, we use the final coordinate system:
- x axis: left to right (width)  => Loft extrusion axis
- y axis: front to back (depth)  => Profile horizontal axis
- z axis: up to down (height)    => Profile vertical axis
"""


@singleton
@inject
@dataclass
class BodyProfile:
    model: BodyModel

    def __call__(self, x: float) -> Profile:
        return Profile(
            upper=lambda y: self.model.top_z(x, y),
            lower=lambda y: -self.model.parameters.body.height,
            span=(
                self.model.start_y(x),
                self.model.end_y(),
            ),
            segments=400,
            breakpoints=[self.model.thumb_section.start_y()],
        )


@singleton
@inject
@dataclass
class Body:
    cap_cad: CapCAD
    model: BodyModel
    profile: BodyProfile

    def assembly(self):
        return loft(
            self.profile,
            span=(self.model.start_x(), self.model.end_x()),
            breakpoints=[self.model.end_x() - self.model.thumb_section.width()],
            fn=200,
        ).rotate([90, 0, 90])


if __name__ == "__main__":
    body = injector.get(Body)
    body_cad = body.assembly()
    body_cad = osc.color(body_cad, "#333333")
    body_cad = body_cad | body.cap_cad.assembly_grid()
    body_cad.show()
