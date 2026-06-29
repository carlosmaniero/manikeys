import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.rj45 import RJ45Model
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ45AdapterFrontCAD(ManifoldObject):
    model: RJ45Model

    @property
    def front(self) -> M:
        return M.cube(
            self.model.front,
            center=True,
        ).translate(self.model.front_coords)

    @property
    def housing(self) -> M:
        return M.cube(
            self.model.housing,
            center=True,
        ).translate(self.model.housing_coords)

    @property
    def screw_holes(self) -> M:
        holes = M()
        for coords in self.model.front_screw_hole_coords:
            hole = (
                M.cylinder(
                    radius_low=self.model.screw_hole_radius,
                    radius_high=self.model.screw_hole_radius,
                    height=self.model.screw_hole_height,
                    center=True,
                    circular_segments=60,
                )
                .rotate([90, 0, 0])
                .translate(coords)
            )
            holes += hole
        return holes

    def assemble(self) -> M:
        return self.front - self.housing - self.screw_holes


if __name__ == "__main__":
    adapter = injector.get(RJ45AdapterFrontCAD)
    adapter.program(sys.argv)
