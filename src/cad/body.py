from __future__ import annotations
import sys
import os
import numpy as np
from injector import inject, singleton
import pyvista as pv
from models.body import LegacyBodyModel
from numpy_ext import map_meshgrid
from pyvista_ext import create_full_surface, VistaObject
from context import injector

SLICES = int(os.getenv("SLICES", 800))


@singleton
@inject
class BodyCAD(VistaObject):
    def __init__(self, model: LegacyBodyModel):
        self.model = model

    def assemble(self) -> pv.PolyData:
        xrange = np.linspace(
            self.model.start_x(), self.model.end_x(), SLICES, endpoint=True
        )

        def yfn(x_arr):
            start_y = np.full_like(x_arr, self.model.start_y())
            end_y = np.full_like(x_arr, self.model.end_y())
            return np.linspace(start_y, end_y, SLICES, axis=-1)

        x, y = map_meshgrid(xrange, yfn)

        top_z_func = np.vectorize(self.model.top_z)
        top_z = top_z_func(x, y)
        bottom_z = np.full_like(x, self.model.min_z)

        return create_full_surface(x, y, top_z, bottom_z)


if __name__ == "__main__":
    body = injector.get(BodyCAD)
    body.program(sys.argv)
