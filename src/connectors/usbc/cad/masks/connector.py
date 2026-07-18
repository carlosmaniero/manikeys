from __future__ import annotations
from globals.wall.parameters import WallParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from connectors.usbc.model import USBCModel
from core.manifold_ext.helpers import capsule
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCConnectorMaskCAD(ManifoldObject):
    wall_parameters: WallParameters
    model: USBCModel

    @property
    def thickness(self) -> float:
        return self.wall_parameters.thickness

    def assemble(self) -> manifold3d.Manifold:
        wall_thickness = self.thickness + self.model.error_margin

        depth = self.model.connector_depth + wall_thickness
        height = self.model.connector_height + self.model.error_margin * 2
        width = self.model.connector_width + self.model.error_margin * 2

        return (
            capsule(
                [width, height, depth],
                circular_segments=60,
            )
            .rotate([90, 0, 0])
            .translate(
                [
                    0,
                    self.model.pcb_width / 2
                    + depth / 2
                    - self.model.connector_depth
                    + 1.5,
                    -self.model.pcb_height / 2
                    - self.model.connector_height / 2,
                ]
            )
        )


if __name__ == "__main__":
    mask = injector.get(USBCConnectorMaskCAD)
    mask.program(sys.argv)
