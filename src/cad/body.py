from dataclasses import dataclass
from models.layout import Layout
from models.parameters import Parameters
from injector import inject
from context import injector
from openscad_ext.loft import loft, Profile
from cad.cap import CapCAD
import math
import openscad as osc

"""
The body is created using a loft that is then rotated [90, 0, 90].
To make the math intuitive, we use the final coordinate system:
- x axis: left to right (width)  => Loft extrusion axis
- y axis: front to back (depth)  => Profile horizontal axis
- z axis: up to down (height)    => Profile vertical axis
"""


@inject
@dataclass
class Body:
    layout: Layout
    parameters: Parameters
    cap_cad: CapCAD

    def assembly(self):
        return loft(
            lambda x: Profile(
                upper=lambda y: self._profile_callback(x, y),
                lower=lambda y: -self.parameters.body.height,
                span=(
                    self._get_start_y(x),
                    self._get_end_y(x),
                ),
                segments=200,
            ),
            span=(self._get_start_x(), self._get_end_x()),
            fn=20,
        ).rotate([90, 0, 90])

    def _thumb_section_width(self) -> float:
        return (self.parameters.caps.size + self.parameters.caps.gap) * 3

    def _thumb_section_height(self) -> float:
        return (self.parameters.caps.size + self.parameters.caps.gap) * 2

    def _caps_start_y(self) -> float:
        return (
            self.layout.positioning.top[1]
            - self.parameters.caps.size
            - self.parameters.caps.gap
        )

    def _get_start_y(self, x: float) -> float:
        delta = 0

        if x >= self._get_end_x() - self._thumb_section_width():
            delta = self._thumb_section_width()

        return self._caps_start_y() - delta

    def _caps_end_y(self) -> float:
        return (
            self.layout.positioning.bottom[1]
            + self.parameters.caps.size
            + self.parameters.caps.gap
        )

    def _get_end_y(self, x: float) -> float:
        return self._caps_end_y()

    def _get_start_x(self) -> float:
        return -self.parameters.caps.size - self.parameters.caps.gap

    def _get_end_x(self) -> float:
        return 180 + self._get_start_x()

    def _profile_callback(self, x: float, y: float) -> float:
        return 0


if __name__ == "__main__":
    body = injector.get(Body)
    body_cad = body.assembly()
    body_cad = osc.color(body_cad, "#333333")
    body_cad = body_cad | body.cap_cad.assembly_grid()
    body_cad.show()
