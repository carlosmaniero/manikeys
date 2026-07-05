from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from assembly.base_plate.model import BasePlateModel
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class BasePlateCAD(ManifoldObject):
    model: BasePlateModel

    def cable_paths(self) -> manifold3d.Manifold:
        outsite = manifold3d.Manifold.cylinder(
            radius_low=self.model.cable_path_radius,
            height=self.model.cable_path_height,
            circular_segments=32,
            center=True,
        )
        inside = manifold3d.Manifold.cylinder(
            radius_low=self.model.cable_path_inner_radius,
            height=self.model.cable_path_height,
            circular_segments=32,
            center=True,
        )
        mask = manifold3d.Manifold.cube(
            self.model.cable_path_mask_dimensions,
            center=True,
        ).translate(self.model.cable_path_mask_coords)

        single_path = (outsite - inside - mask).rotate([0, -90, 0])
        paths = []
        for coords in self.model.cable_path_grid_coords:
            paths.append(single_path.translate(coords))

        return (
            manifold3d.Manifold.batch_boolean(paths, manifold3d.OpType.Add)
            if paths
            else manifold3d.Manifold()
        )

    def screw_head_holes(self) -> manifold3d.Manifold:
        holes = []
        cyl = manifold3d.Manifold.cylinder(
            radius_low=self.model.screw_head_radius,
            height=self.model.screw_head_height,
            circular_segments=32,
            center=False,
        )
        for coords in self.model.screw_head_coords:
            holes.append(cyl.translate(coords))
        return (
            manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)
            if holes
            else manifold3d.Manifold()
        )

    def screw_holes(self) -> manifold3d.Manifold:
        holes = []
        cyl = manifold3d.Manifold.cylinder(
            radius_low=self.model.screw_hole_radius,
            height=self.model.screw_hole_height,
            circular_segments=32,
            center=False,
        )
        for coords in self.model.screw_hole_coords:
            holes.append(cyl.translate(coords))
        return (
            manifold3d.Manifold.batch_boolean(holes, manifold3d.OpType.Add)
            if holes
            else manifold3d.Manifold()
        )

    def assemble(self) -> manifold3d.Manifold:
        bottom = manifold3d.Manifold.cube(
            self.model.dimensions,
            center=False,
        ).translate(self.model.coords)

        cavity = manifold3d.Manifold.cube(
            self.model.cavity_dimensions,
            center=False,
        ).translate(self.model.cavity_coords)

        pro_case = (
            load_stl_to_manifold(
                "build/components/arduino_pro_micro_case/cad/housing.stl"
            )
            .rotate([0, 0, 90])
            .translate(self.model.pro_case_coords)
        )
        nano_case = (
            load_stl_to_manifold(
                "build/components/arduino_nano_case/cad/case.stl"
            )
            .rotate([0, 0, 90])
            .translate(self.model.nano_case_coords)
        )

        return (
            bottom
            - cavity
            - self.screw_holes()
            - self.screw_head_holes()
            + pro_case
            + nano_case
            + self.cable_paths()
        )


if __name__ == "__main__":
    base_plate = injector.get(BasePlateCAD)
    base_plate.program(sys.argv)
