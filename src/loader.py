from __future__ import annotations
import openscad as osc
from pathlib import Path
import manifold3d
import pyvista as pv
from concurrent.futures import ThreadPoolExecutor


def load_stl(path: str) -> osc.PyOpenSCAD:
    absolute_path = str(Path(path).resolve())

    if not Path(absolute_path).exists():
        raise FileNotFoundError(f"STL file not found: {absolute_path}")

    return osc.osimport(absolute_path)


def load_stl_to_manifold(path: str) -> manifold3d.Manifold:
    absolute_path = str(Path(path).resolve())

    if not Path(absolute_path).exists():
        raise FileNotFoundError(f"STL file not found: {absolute_path}")

    pd = pv.read(absolute_path)
    # Ensure it's triangulated
    pd = pd.triangulate()

    return manifold3d.Manifold(
        manifold3d.Mesh(
            vert_properties=pd.points.astype("float32"),
            tri_verts=pd.faces.reshape(-1, 4)[:, 1:].astype("int32"),
        )
    )


def load_many_stl_to_manifold(paths: list[str]) -> list[manifold3d.Manifold]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(load_stl_to_manifold, paths))
