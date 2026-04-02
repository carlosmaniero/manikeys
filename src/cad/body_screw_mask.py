from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.body_screw_placement import BodyScrewPlacementModel
from openscad_ext.object import OSCObject


@singleton
@inject
@dataclass
class BodyScrewMaskCAD(OSCObject):
    model: BodyScrewPlacementModel

    def assemble(self) -> osc.PyOpenSCAD:
        cubes = []
        for x, y in self.model.get_mask_points():
            cube = osc.cube(
                [
                    self.model.mask_size,
                    self.model.mask_size,
                    self.model.mask_height,
                ],
                center=False,
            )
            cube = osc.translate(cube, [x, y, self.model.mask_z])
            cubes.append(cube)

        return osc.union(*cubes)


if __name__ == "__main__":
    body_screw_mask = injector.get(BodyScrewMaskCAD)
    body_screw_mask.program(sys.argv)
