from __future__ import annotations
import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from models.parameters import SwitchesParameters
from core.manifold_ext.helpers import rounded_box
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
        w = p.size + p.border * 2
        d = p.size + p.border * 2
        h = p.thickness
        r = p.border / 4

        obj = rounded_box([w, d, h], r)

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
