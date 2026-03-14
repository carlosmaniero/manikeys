from __future__ import annotations
import pyvista as pv
import numpy as np
import numpy.typing as npt
from cad.object import Object


class VistaObject(Object[pv.PolyData]):
    def save(self, path: str):
        obj = self.assemble()
        obj.save(path)

    def show(self):
        obj = self.assemble()
        obj.plot()


def create_full_surface(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    top_z: npt.NDArray[np.float64],
    bottom_z: npt.NDArray[np.float64],
) -> pv.PolyData:
    top_surface = pv.StructuredGrid(x, y, top_z).extract_surface(algorithm=None)
    bottom_surface = pv.StructuredGrid(x, y, bottom_z).extract_surface(
        algorithm=None
    )
    return top_surface + bottom_surface
