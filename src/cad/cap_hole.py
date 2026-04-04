import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from models.parameters import Parameters
from manifold_ext.object import ManifoldObject
from context import injector


@singleton
@inject
@dataclass
class CapHoleCAD(ManifoldObject):
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        return manifold3d.Manifold.cube(
            [
                self.parameters.caps.size,
                self.parameters.caps.size,
                self.parameters.caps.thickness * 5
                + self.parameters.globals.diff_offset * 2,
            ],
            center=True,
        )


if __name__ == "__main__":
    cap_hole = injector.get(CapHoleCAD)
    cap_hole.program(sys.argv)
