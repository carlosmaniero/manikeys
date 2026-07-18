from __future__ import annotations
import sys
from dataclasses import dataclass
import manifold3d
from injector import inject, singleton
from models.parameters import SwitchesParameters
from globals.wall.parameters import WallParameters
from core.manifold_ext.object import ManifoldObject
from core.context import injector
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class SwitchHoleDecoratorShellCAD(ManifoldObject):
    switches_parameters: SwitchesParameters
    wall_parameters: WallParameters

    @property
    def cable_radius(self) -> float:
        return 1

    @property
    def cable_path_wall_thickness(self) -> float:
        return 1

    @property
    def col_cable_path_wall_thickness(self) -> float:
        return 3

    @property
    def col_cable_path_wall(self) -> manifold3d.Manifold:
        radius = self.cable_radius + self.col_cable_path_wall_thickness
        height = self.cable_radius + self.col_cable_path_wall_thickness
        outer = manifold3d.Manifold.cylinder(
            radius_low=radius,
            height=height,
            center=True,
            circular_segments=32,
        ) + manifold3d.Manifold.cube(
            [radius * 2, radius, height],
            center=True,
        ).translate([0, radius / 2, 0])
        return outer.rotate([90, 0, 90]).translate(
            [
                -self.switches_parameters.size / 2
                - self.switches_parameters.border,
                self.switches_parameters.size / 4
                - self.wall_parameters.thickness,
                -self.switches_parameters.thickness
                - (self.cable_radius + self.cable_path_wall_thickness) * 2,
            ]
        )

    @property
    def col_cable_path_inner(self) -> manifold3d.Manifold:
        height = self.cable_radius + self.col_cable_path_wall_thickness
        inner = manifold3d.Manifold.cylinder(
            radius_low=self.cable_radius,
            height=height,
            center=True,
            circular_segments=32,
        )
        return inner.rotate([90, 0, 90]).translate(
            [
                -self.switches_parameters.size / 2
                - self.switches_parameters.border,
                self.switches_parameters.size / 4
                + 2
                - self.wall_parameters.thickness,
                -self.switches_parameters.thickness
                - (self.cable_radius + self.cable_path_wall_thickness) * 2
                - 1,
            ]
        )

    @property
    def cable_path_wall(self) -> manifold3d.Manifold:
        radius = self.cable_radius + self.cable_path_wall_thickness
        height = self.switches_parameters.size * 0.8
        outer = manifold3d.Manifold.cylinder(
            radius_low=radius,
            height=height,
            center=True,
            circular_segments=32,
        ) + manifold3d.Manifold.cube(
            [radius * 2, radius, height],
            center=True,
        ).translate([0, radius / 2, 0])
        return outer.rotate([90, 0, 0]).translate(
            [
                -self.switches_parameters.size / 2
                - self.switches_parameters.border,
                -self.switches_parameters.size / 4
                + self.wall_parameters.thickness,
                -self.switches_parameters.thickness,
            ]
        )

    @property
    def cable_path_inner(self) -> manifold3d.Manifold:
        height = self.switches_parameters.size * 0.8
        inner = manifold3d.Manifold.cylinder(
            radius_low=self.cable_radius,
            height=height,
            center=True,
            circular_segments=32,
        )
        return inner.rotate([90, 0, 0]).translate(
            [
                -self.switches_parameters.size / 2
                - self.switches_parameters.border,
                -self.switches_parameters.size / 4
                + self.wall_parameters.thickness,
                -self.switches_parameters.thickness,
            ]
        )

    def assemble(self) -> manifold3d.Manifold:
        parameters = self.switches_parameters

        width = parameters.size + parameters.border + parameters.border_shell
        depth = parameters.size + parameters.border * 2
        height = parameters.thickness

        obj = manifold3d.Manifold.cube([width, depth, height], center=True)

        obj = obj.translate(
            [0, 0, -(parameters.thickness / 2 - parameters.outer.thickness)]
        )

        mask = load_stl_to_manifold(
            "build/switches/socket/cad/hot_swap_placement_mask.stl"
        )

        mask = mask.rotate([180, 0, 180]).translate(
            [0, 0, parameters.outer.thickness]
        )

        switch_hole = load_stl_to_manifold("build/switches/cad/switch_hole.stl")
        walls = obj + manifold3d.Manifold.hull(
            self.cable_path_wall + self.col_cable_path_wall
        )
        masks = (
            switch_hole
            + mask
            + self.cable_path_inner
            + self.col_cable_path_inner
        )
        return walls - masks


if __name__ == "__main__":
    switch_hole_decorator_shell = injector.get(SwitchHoleDecoratorShellCAD)
    switch_hole_decorator_shell.program(sys.argv)
