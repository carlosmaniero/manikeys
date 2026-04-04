from __future__ import annotations
import os
from typing import Sequence
import manifold3d
import pyvista as pv
import numpy as np
from cad.object import Object
import sys


class ManifoldObject(Object[manifold3d.Manifold]):
    def save(self, path: str):
        manifold = self.assemble()
        mesh = manifold.to_mesh()

        pd = pv.PolyData(
            mesh.vert_properties,
            np.hstack(
                [np.full((mesh.tri_verts.shape[0], 1), 3), mesh.tri_verts]
            ),
        )
        pd.save(path)

    def show(self):
        manifold = self.assemble()
        mesh = manifold.to_mesh()

        pd = pv.PolyData(
            mesh.vert_properties,
            np.hstack(
                [np.full((mesh.tri_verts.shape[0], 1), 3), mesh.tri_verts]
            ),
        )

        plotter = pv.Plotter()
        plotter.add_mesh(pd, color="tan")
        plotter.show_grid()
        plotter.add_axes()
        plotter.show()

    def program(self, argv: Sequence[str]):
        try:
            super().program(argv)
        finally:
            sys.stdout.flush()
            os._exit(0)
