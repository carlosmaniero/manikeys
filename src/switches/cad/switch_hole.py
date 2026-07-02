from models.parameters import SwitchesParameters
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.manifold_ext.object import ManifoldObject
from core.context import injector


@singleton
@inject
@dataclass
class SwitchHoleCAD(ManifoldObject):
    switches_parameters: SwitchesParameters

    def assemble(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.switches_parameters.size,
                self.switches_parameters.size,
                self.switches_parameters.thickness * 4,
            ],
            center=True,
        )


if __name__ == "__main__":
    switch_hole = injector.get(SwitchHoleCAD)
    switch_hole.program(sys.argv)
