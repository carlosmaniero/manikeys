from __future__ import annotations
import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from connectors.rj45_tabs.model import AdapterModel


@singleton
@inject
@dataclass
class AdapterCAD(ManifoldObject):
    model: AdapterModel

    @property
    def body(self):
        return M.cube(self.model.full_body_size, center=True)

    @property
    def exposed_hole(self):
        return M.cube(
            self.model.exposed_body_hole_full_size, center=True
        ).translate(self.model.exposed_body_hole_coords)

    @property
    def tabs_pocket(self):
        cylinder = M.cylinder(
            self.model.tabs_pocket_depth,
            self.model.tabs_pocket_radius,
            circular_segments=32,
            center=True,
        ).translate(self.model.tabs_pocket_coords)

        return M.hull(cylinder + cylinder.mirror([-1, 0, 0]))

    @property
    def screws_pocket(self):
        cylinder = M.cylinder(
            self.model.screw_depth,
            self.model.screw_radius,
            circular_segments=32,
            center=True,
        ).translate(self.model.screw_coords)

        return cylinder + cylinder.mirror([-1, 0, 0])

    @property
    def screw_heads_pocket(self):
        cylinder = M.cylinder(
            self.model.screw_head_depth,
            self.model.screw_head_radius,
            circular_segments=32,
            center=True,
        ).translate(self.model.screw_head_coords)

        return cylinder + cylinder.mirror([-1, 0, 0])

    @property
    def body_pocket(self):
        return M.cube(self.model.body_pocket_full_size, center=True).translate(
            self.model.body_pocket_coords
        )

    def assemble(self) -> M:
        return (
            self.body
            - self.exposed_hole
            - self.tabs_pocket
            - self.screws_pocket
            - self.screw_heads_pocket
            - self.body_pocket
        )


if __name__ == "__main__":
    adapter = injector.get(AdapterCAD)
    adapter.program(sys.argv)
