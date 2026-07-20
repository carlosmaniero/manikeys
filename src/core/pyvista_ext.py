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


def normalize_to_surface(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    z: npt.NDArray[np.float64] | float,
) -> pv.PolyData:
    if isinstance(z, (int, float)):
        nx, ny = x.shape
        perimeter_x = []
        perimeter_y = []
        for j in range(ny):
            perimeter_x.append(x[0, j])
            perimeter_y.append(y[0, j])
        for i in range(1, nx):
            perimeter_x.append(x[i, ny - 1])
            perimeter_y.append(y[i, ny - 1])
        for j in range(ny - 2, -1, -1):
            perimeter_x.append(x[nx - 1, j])
            perimeter_y.append(y[nx - 1, j])
        for i in range(nx - 2, 0, -1):
            perimeter_x.append(x[i, 0])
            perimeter_y.append(y[i, 0])
        pts = np.column_stack(
            (perimeter_x, perimeter_y, np.full_like(perimeter_x, z))
        )
        faces = [len(pts)] + list(range(len(pts)))
        return pv.PolyData(pts, faces).triangulate()
    return pv.StructuredGrid(x, y, z).extract_surface(algorithm=None)


def create_full_surface(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    top_z: npt.NDArray[np.float64] | float,
    bottom_z: npt.NDArray[np.float64] | float,
) -> pv.PolyData:
    top_surface = normalize_to_surface(x, y, top_z)
    bottom_surface = normalize_to_surface(x, y, bottom_z)
    return top_surface + bottom_surface
