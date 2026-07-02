from __future__ import annotations
from globals.wall.parameters import WallParameters
from structure.body.parameters import BodyParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from switches.socket.mount.models import MountCavityModel
from connectors.pogo.models import PogoPinModel
from structure.body.models import BodyModel
from core.manifold_ext.object import ManifoldObject
from core.loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class CablePath(ManifoldObject):
    model: MountCavityModel
    pogo_model: PogoPinModel
    body_model: BodyModel
    wall_parameters: WallParameters
    body_parameters: BodyParameters

    @property
    def pogo_location_mask(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            size=[
                self.radius * 2,
                self.wall_parameters.thickness * 2,
                self.body_model.height * 2,
            ],
            center=True,
        )

    @property
    def length(self) -> float:
        return 100

    @property
    def pogo_mask(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            size=[
                self.pogo_model.adapter_width,
                self.pogo_model.adapter_length,
                self.pogo_model.adapter_height * 2,
            ],
            center=True,
        ).rotate([90, 0, 0])

    @property
    def pogo_adapter(self):
        return load_stl_to_manifold(
            "build/connectors/pogo/cad/pogo_pin_adapter.stl"
        ).rotate([90, 0, 180])

    @property
    def pogo_adapters(self) -> manifold3d.Manifold:
        return self.pogo_adapter.translate(
            [0, -self.pogo_model.adapter_height / 2 - 0.5, 0]
        ) + self.pogo_adapter.rotate([0, 0, 180]).translate(
            [0, self.pogo_model.adapter_height / 2 + 0.5, 0]
        )

    @property
    def radius(self) -> float:
        return self.pogo_model.adapter_width / 2

    def assemble(self) -> manifold3d.Manifold:
        thickness = self.wall_parameters.thickness
        height = self.body_parameters.height

        cylinder = manifold3d.Manifold.cylinder(
            radius_low=self.radius,
            height=self.length,
            center=True,
        ).rotate([90, 0, 0])

        return (
            manifold3d.Manifold.hull(
                cylinder + cylinder.translate([0, 0, -height * 2])
            )
            - self.pogo_location_mask
            + self.pogo_mask
            - self.pogo_adapters
        ).translate(
            [
                self.model.end_x() - self.radius - thickness * 3,
                self.model.divider_y,
                self.body_model.bottom_z + thickness * 2,
            ]
        )


if __name__ == "__main__":
    cable_path = injector.get(CablePath)
    cable_path.program(sys.argv)
