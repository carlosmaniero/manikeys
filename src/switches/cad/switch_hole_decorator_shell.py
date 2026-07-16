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
class SwitchHoleDecoratorShellCAD(ManifoldObject):
    switches_parameters: SwitchesParameters

    def assemble(self) -> manifold3d.Manifold:
        p = self.switches_parameters
        w = p.size + p.border + p.border_shell
        d = p.size + p.border * 2
        h = p.thickness

        obj = manifold3d.Manifold.cube([w, d, h], center=True)

        obj = obj.translate([0, 0, -(p.thickness / 2 - p.outer.thickness)])

        mask = load_stl_to_manifold(
            "build/switches/socket/cad/hot_swap_placement_mask.stl"
        )
        mask = mask.rotate([180, 0, 180]).translate([0, 0, p.outer.thickness])

        switch_hole = load_stl_to_manifold("build/switches/cad/switch_hole.stl")
        return obj - switch_hole - mask


if __name__ == "__main__":
    switch_hole_decorator_shell = injector.get(SwitchHoleDecoratorShellCAD)
    switch_hole_decorator_shell.program(sys.argv)
