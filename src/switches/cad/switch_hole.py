import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from models.parameters import Parameters
from core.manifold_ext.object import ManifoldObject
from core.context import injector


@singleton
@inject
@dataclass
class SwitchHoleCAD(ManifoldObject):
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.parameters.switches.size,
                self.parameters.switches.size,
                self.parameters.switches.thickness * 2,
            ],
            center=True,
        )


if __name__ == "__main__":
    switch_hole = injector.get(SwitchHoleCAD)
    switch_hole.program(sys.argv)
