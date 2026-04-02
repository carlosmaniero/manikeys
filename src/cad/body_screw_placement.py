from __future__ import annotations
import sys
import os
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl
from models.body_screw_placement import BodyScrewPlacementModel
from openscad_ext.object import OSCObject

DEBUG = os.getenv("DEBUG", "false") == "true"


@singleton
@inject
@dataclass
class BodyScrewPlacementCAD(OSCObject):
    model: BodyScrewPlacementModel

    def assemble(self) -> osc.PyOpenSCAD:
        cubes = []
        for x, y in self.model.points:
            cube = osc.cube(
                [
                    self.model.cube_size,
                    self.model.cube_size,
                    self.model.cube_height,
                ],
                center=False,
            )
            cube = osc.translate(cube, [x, y, self.model.z])
            cubes.append(cube)

        body = load_stl("build/cad/body.stl")

        return osc.intersection(osc.union(*cubes), body)


if __name__ == "__main__":
    body_screw_placement = injector.get(BodyScrewPlacementCAD)
    body_screw_placement.program(sys.argv)
