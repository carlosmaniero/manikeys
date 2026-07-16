from __future__ import annotations
import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from models.parameters import SwitchesParameters
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class SwitchHoleDecoratorCAD(ManifoldObject):
    switches_parameters: SwitchesParameters

    def assemble(self) -> manifold3d.Manifold:
        p = self.switches_parameters
        fn = 20
        w = p.size + p.border * 2
        d = p.size + p.border * 2
        h = p.thickness
        r = p.border / 4

        # Rounded cube using cylinder hull
        cyl = manifold3d.Manifold.cylinder(
            h, r, center=True, circular_segments=fn
        )

        x_off = w / 2 - r
        y_off = d / 2 - r
        c1 = cyl.translate([x_off, y_off, 0])
        c2 = cyl.translate([-x_off, y_off, 0])
        c3 = cyl.translate([x_off, -y_off, 0])
        c4 = cyl.translate([-x_off, -y_off, 0])
        obj = (c1 + c2 + c3 + c4).hull()

        squared_bottom = manifold3d.Manifold.cube(
            [
                p.size + p.border * 2,
                p.size + p.border * 2,
                p.thickness / 2,
            ],
            center=True,
        )
        squared_bottom = squared_bottom.translate([0, 0, -p.thickness / 4])

        obj = obj + squared_bottom

        obj = obj.translate([0, 0, -(p.thickness / 2 - p.outer.thickness)])

        switch_hole = load_stl_to_manifold("build/switches/cad/switch_hole.stl")
        return obj - switch_hole


if __name__ == "__main__":
    switch_hole_decorator = injector.get(SwitchHoleDecoratorCAD)
    switch_hole_decorator.program(sys.argv)
