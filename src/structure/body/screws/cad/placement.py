from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from structure.body.screws.models import ScrewPlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class ScrewPlacementCAD(ManifoldObject):
    model: ScrewPlacementModel

    def assemble(self) -> manifold3d.Manifold:
        standoffs = []
        for x, y in self.model.points:
            standoff = manifold3d.Manifold.cylinder(
                self.model.standoff_height,
                self.model.standoff_size,
                center=True,
            ).translate(
                [
                    x + self.model.standoff_size / 2,
                    y + self.model.standoff_size / 2,
                    self.model.z + self.model.standoff_height / 2,
                ]
            )

            standoffs.append(standoff)

        body = load_stl_to_manifold("build/structure/body/shape.stl")

        return (
            manifold3d.Manifold.batch_boolean(standoffs, manifold3d.OpType.Add)
            ^ body
        )


if __name__ == "__main__":
    placement = injector.get(ScrewPlacementCAD)
    placement.program(sys.argv)
