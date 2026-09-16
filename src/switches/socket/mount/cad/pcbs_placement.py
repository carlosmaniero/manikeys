from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from core.manifold_ext.helpers import rounded_box, path_extrude
from switches.socket.mount.model import PcbsPlacementModel


@singleton
@inject
@dataclass
class PcbsPlacementCAD(ManifoldObject):
    model: PcbsPlacementModel

    def connecting_paths(self) -> manifold3d.Manifold:
        cross_section = manifold3d.CrossSection.square(
            [
                self.model.parameters.thickness,
                self.model.parameters.wall_margin,
            ],
            center=True,
        )
        paths = []
        for ctrl_pts in self.model.connection_paths_control_points:
            paths.append(path_extrude(cross_section, ctrl_pts))

        return manifold3d.Manifold.batch_boolean(paths, manifold3d.OpType.Add)

    def arduinos_assembly(self) -> manifold3d.Manifold:
        pro_case = (
            self.deps.stls[
                "build/components/arduino_pro_micro_case/cad/housing.stl"
            ]
            .rotate([180, 0, 90])
            .translate(self.model.pro_case_coords)
        )
        nano_case = (
            self.deps.stls["build/components/arduino_nano_case/cad/case.stl"]
            .rotate([180, 0, 90])
            .translate(self.model.nano_case_coords)
        )

        cases_base = rounded_box(
            list(self.model.cases_base_dimensions),
            self.model.fillet_radius,
            circular_segments=100,
            center=True,
        ).translate(self.model.cases_base_center)

        return cases_base + pro_case + nano_case

    def assemble(self) -> manifold3d.Manifold:
        pcb = manifold3d.Manifold.cube(
            self.model.dimensions, center=False
        ).translate(self.model.coords)

        hole_cylinders = []
        for hx, hy in self.model.screw_cylinder_model.hole_placements:
            hole_cyl = manifold3d.Manifold.cylinder(
                self.model.parameters.thickness * 3,
                self.model.screw_cylinder_model.hole_radius,
                circular_segments=100,
                center=True,
            ).translate(
                [
                    hx,
                    hy,
                    self.model.coords[2] + self.model.parameters.thickness / 2,
                ]
            )
            hole_cylinders.append(hole_cyl)

        holes = manifold3d.Manifold.batch_boolean(
            hole_cylinders, manifold3d.OpType.Add
        )

        mask_cylinders = []
        for cx, cy in self.model.cavity_mask_placements:
            mask_cyl = manifold3d.Manifold.cylinder(
                self.model.parameters.thickness * 3,
                self.model.cavity_mask_radius,
                circular_segments=100,
                center=True,
            ).translate(
                [
                    cx,
                    cy,
                    self.model.coords[2] + self.model.parameters.thickness / 2,
                ]
            )
            mask_cylinders.append(mask_cyl)

        cavity_masks = manifold3d.Manifold.batch_boolean(
            mask_cylinders, manifold3d.OpType.Add
        )

        inner_cut = rounded_box(
            list(self.model.inner_cut_dimensions),
            self.model.fillet_radius,
            circular_segments=100,
            center=True,
        ).translate(self.model.inner_cut_center)

        return (
            pcb
            - holes
            - cavity_masks
            - inner_cut
            + self.connecting_paths()
            + self.arduinos_assembly()
        )


if __name__ == "__main__":
    pcbs_placement = injector.get(PcbsPlacementCAD)
    pcbs_placement.program(sys.argv)
