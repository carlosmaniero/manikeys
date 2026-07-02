import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from connectors.rj45.model import RJ45Model
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ45AdapterCAD(ManifoldObject):
    model: RJ45Model

    @property
    def body(self) -> M:
        return M.cube(
            self.model.body,
            center=True,
        )

    @property
    def housing(self) -> M:
        return M.cube(
            self.model.housing,
            center=True,
        ).translate(self.model.housing_coords)

    @property
    def socket_holes(self) -> M:
        holes = M()
        for coords in self.model.socket_holes_coords:
            bottom_cylinder = M.cylinder(
                radius_low=self.model.socket_hole_bottom_radius,
                radius_high=self.model.socket_hole_bottom_radius,
                height=self.model.socket_hole_bottom_height,
                center=True,
                circular_segments=60,
            ).translate(self.model.socket_hole_bottom_coords)

            top_cylinder = M.cylinder(
                radius_low=self.model.socket_hole_top_radius,
                radius_high=self.model.socket_hole_top_radius,
                height=self.model.socket_hole_top_height,
                center=True,
                circular_segments=60,
            ).translate(self.model.socket_hole_top_coords)

            hole = (bottom_cylinder + top_cylinder).translate(coords)
            holes += hole
        return holes

    @property
    def pins_pocket(self) -> M:
        return M.cube(
            self.model.pins_pocket,
            center=True,
        ).translate(self.model.pins_pocket_coords)

    @property
    def front_pocket(self) -> M:
        return M.cube(
            self.model.front_pocket,
            center=True,
        ).translate(self.model.front_pocket_coords)

    @property
    def screw_tabs(self) -> M:
        return M.cube(
            self.model.screw_tabs,
            center=True,
        ).translate(self.model.screw_tabs_coords)

    @property
    def screw_holes(self) -> M:
        holes = M()
        for coords in self.model.screw_hole_coords:
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
        return (
            self.body
            + self.screw_tabs
            - self.housing
            - self.socket_holes
            - self.pins_pocket
            - self.front_pocket
            - self.screw_holes
        )


if __name__ == "__main__":
    adapter = injector.get(RJ45AdapterCAD)
    adapter.program(sys.argv)
