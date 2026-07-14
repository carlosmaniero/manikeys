from __future__ import annotations
import sys
import os
import numpy as np
from injector import inject, singleton
from dataclasses import dataclass
import pyvista as pv
from structure.body.models import BodyInnerModel
from core.numpy_ext import map_meshgrid
from core.pyvista_ext import create_full_surface, VistaObject
from core.context import injector

SLICES = int(os.getenv("SLICES", 800))


@singleton
@inject
@dataclass
class BodyCavityCAD(VistaObject):
    model: BodyInnerModel

    def show(self):
        inner = self.assemble()

        from cad.body import BodyCAD

        body_cad = injector.get(BodyCAD)
        body = body_cad.assemble()

        plotter = pv.Plotter()

        plotter.add_mesh(body, color="tan", opacity=0.25)
        plotter.add_mesh(inner, color="cyan")

        plotter.show_grid()  # type: ignore
        plotter.add_axes()  # type: ignore

        plotter.show()

    def assemble(self) -> pv.PolyData:
        xrange = np.linspace(
            self.model.start_x(),
            self.model.end_x(),
            SLICES,
            endpoint=True,
        )

        def yfn(x_arr):
            start_y = np.full_like(x_arr, self.model.start_y())
            end_y = np.full_like(x_arr, self.model.end_y())
            return np.linspace(start_y, end_y, SLICES, axis=-1)

        x, y = map_meshgrid(xrange, yfn)

        top_z = self.model.z(x, y)
        return create_full_surface(
            x, y, top_z, -self.model.body_parameters.height
        )


if __name__ == "__main__":
    body_cavity = injector.get(BodyCavityCAD)
    body_cavity.program(sys.argv)
