from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from models.socket_placement import SocketPlacementInner
from models.pogo_pin import PogoPinModel
from manifold_ext.object import ManifoldObject
from loader import load_stl_to_manifold


@singleton
@inject
@dataclass
class CablePath(ManifoldObject):
    model: SocketPlacementInner
    pogo_model: PogoPinModel
    parameters: Parameters

    @property
    def pogo_location_mask(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            size=[
                self.radius * 2,
                self.parameters.body.thickness * 2,
                self.radius * 2,
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
            "build/cad/connectors/pogo_pin_adapter.stl"
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
        return self.parameters.body.cabe_hole_radius

    def assemble(self) -> manifold3d.Manifold:
        thickness = self.parameters.body.thickness
        height = self.parameters.body.height

        return (
            manifold3d.Manifold.cylinder(
                radius_low=self.radius,
                height=self.length,
                center=True,
            ).rotate([90, 0, 0])
            - self.pogo_location_mask
            + self.pogo_mask
            - self.pogo_adapters
        ).translate(
            [
                self.model.end_x() - self.radius - thickness * 3,
                self.model.sphere.start_y(),
                -(height - self.radius - thickness * 2),
            ]
        )


if __name__ == "__main__":
    cable_path = injector.get(CablePath)
    cable_path.program(sys.argv)
