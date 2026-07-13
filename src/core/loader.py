from __future__ import annotations
from pathlib import Path
import manifold3d
import pyvista as pv
import trimesh
from concurrent.futures import ThreadPoolExecutor


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


def load_stl_to_trimesh(path: str) -> trimesh.Trimesh:
    absolute_path = str(Path(path).resolve())

    if not Path(absolute_path).exists():
        raise FileNotFoundError(f"STL file not found: {absolute_path}")

    return trimesh.load(absolute_path)


def load_many_stl_to_manifold(paths: list[str]) -> list[manifold3d.Manifold]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(load_stl_to_manifold, paths))


def load_many_stl_to_trimesh(paths: list[str]) -> list[trimesh.Trimesh]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(load_stl_to_trimesh, paths))


def load_3mf_to_trimesh(path: str) -> trimesh.Scene:
    absolute_path = str(Path(path).resolve())
    if not Path(absolute_path).exists():
        raise FileNotFoundError(f"3MF file not found: {absolute_path}")

    scene = trimesh.load(absolute_path)

    import zipfile
    import xml.etree.ElementTree as ET

    try:
        with zipfile.ZipFile(absolute_path, "r") as zip_read:
            model_xml = zip_read.read("3D/3dmodel.model")

        root = ET.fromstring(model_xml)
        namespaces = {
            "core": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
        }
        resources = root.find("core:resources", namespaces)
        if resources is not None:
            colors = []
            basemats = resources.find("core:basematerials", namespaces)
            if basemats is not None:
                for base in basemats.findall("core:base", namespaces):
                    colors.append(base.get("displaycolor"))

            mesh_colors = {}
            for obj in resources.findall("core:object", namespaces):
                name = obj.get("name")
                pid = obj.get("pid")
                pindex = obj.get("pindex")
                if name and pid and pindex is not None:
                    idx = int(pindex)
                    if idx < len(colors):
                        mesh_colors[name] = colors[idx]

            for name, mesh in scene.geometry.items():
                if name in mesh_colors:
                    c = mesh_colors[name].lstrip("#")
                    mesh.visual.face_colors = [
                        int(c[i : i + 2], 16) for i in (0, 2, 4)
                    ] + [255]
    except Exception:
        pass

    return scene
