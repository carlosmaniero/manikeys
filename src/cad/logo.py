from __future__ import annotations
import sys
import numpy as np
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from openscad_ext.object import OSCObject
from loader import load_stl
from models.body import BodyModel
from models.parameters import Parameters


@singleton
@inject
@dataclass
class LogoCAD(OSCObject):
    body: BodyModel
    parameters: Parameters

    def assemble(self) -> osc.PyOpenSCAD:
        logo = load_stl("dist/mani-logo.stl")

        logo_w = 15.00
        logo_d = 63.12

        x_start = self.body.divider_x_main
        x_end = self.body.end_x() - self.parameters.body.fillet / 2
        center_x = (x_start + x_end) / 2

        y_start = self.body.divider_y
        y_end = self.body.end_y()
        center_y = (y_start + y_end) / 2

        target_x = center_x - logo_w / 2
        target_y = center_y - logo_d / 2

        target_z = (
            float(self.body.z(np.array([center_x]), np.array([center_y]))[0])
            - 2
        )

        return osc.translate(logo, [target_x, target_y, target_z])


if __name__ == "__main__":
    logo = injector.get(LogoCAD)
    logo.program(sys.argv)
