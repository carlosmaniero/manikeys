from __future__ import annotations
import pyvista as pv
import numpy as np
import numpy.typing as npt
from core.object import Object


class VistaObject(Object[pv.PolyData]):
    def save(self, path: str):
        obj = self.assemble()
        obj.save(path)

    def show(self):
        obj = self.assemble()
        obj.plot()


def normalize_to_grid(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    z: npt.NDArray[np.float64] | float,
) -> pv.StructuredGrid:
    if isinstance(z, (int, float)):
        bz = np.full_like(x, z)
        return pv.StructuredGrid(x, y, bz)
    return pv.StructuredGrid(x, y, z)


def create_full_surface(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    top_z: npt.NDArray[np.float64] | float,
    bottom_z: npt.NDArray[np.float64] | float,
) -> pv.PolyData:
    top_surface = normalize_to_grid(x, y, top_z).extract_surface(algorithm=None)
    bottom_surface = normalize_to_grid(x, y, bottom_z).extract_surface(
        algorithm=None
    )
    return top_surface + bottom_surface
