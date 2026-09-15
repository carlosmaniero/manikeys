import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from connectors.rj45.model import RJ45PlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ45AdapterFrontPlacementCAD(ManifoldObject):
    model: RJ45PlacementModel

    def assemble(self) -> M:
        front = self.deps.stls["build/connectors/rj45/cad/adapter_front.stl"]
        body = self.deps.stls["build/structure/body/shape.stl"]

        placement = front.rotate([0, 0, -90]).translate(
            self.model.translation_coords
        )

        screw_holes = M()
        for coords in self.model.rj45_model.front_screw_hole_coords:
            hole = (
                M.cylinder(
                    radius_low=self.model.rj45_model.screw_hole_radius,
                    radius_high=self.model.rj45_model.screw_hole_radius,
                    height=self.model.rj45_model.screw_hole_height * 4,
                    center=True,
                    circular_segments=60,
                )
                .rotate([90, 0, 0])
                .translate(coords)
            )
            screw_holes += hole

        screw_holes = screw_holes.rotate([0, 0, -90]).translate(
            self.model.translation_coords
        )

        return (placement - screw_holes) ^ body


if __name__ == "__main__":
    placement = injector.get(RJ45AdapterFrontPlacementCAD)
    placement.program(sys.argv)
