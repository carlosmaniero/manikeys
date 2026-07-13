from __future__ import annotations
import os
import sys
from typing import Sequence, Iterator, Union
import trimesh
from core.object import Object
from core.three_mf import get_mesh_color, inject_3mf_metadata


class TrimeshObject(Object[Union[trimesh.Trimesh, trimesh.Scene]]):
    def save(self, path: str):
        obj = self.assemble()
        if isinstance(obj, Iterator):
            meshes = list(obj)
        elif isinstance(obj, trimesh.Scene):
            meshes = list(obj.geometry.values())
        else:
            meshes = [obj]

        # 1. Create a scene with controlled geometry names
        scene = trimesh.Scene()
        mesh_by_name = {}
        for idx, mesh in enumerate(meshes):
            name = mesh.metadata.get("file_name", f"part_{idx}")
            name = os.path.basename(name)
            # Ensure name is unique
            base_name = name
            counter = 1
            while name in mesh_by_name:
                name = f"{base_name}_{counter}"
                counter += 1
            scene.add_geometry(mesh, geom_name=name)
            mesh_by_name[name] = mesh

        # 2. Export standard 3MF via trimesh
        scene.export(path)

        if not path.lower().endswith(".3mf"):
            return

        mesh_colors = {
            name: get_mesh_color(mesh) for name, mesh in mesh_by_name.items()
        }
        inject_3mf_metadata(path, mesh_colors)

    def show(self):
        obj = self.assemble()
        if isinstance(obj, Iterator):
            trimesh.Scene(list(obj)).show()
        else:
            obj.show()

    def program(self, argv: Sequence[str]):
        try:
            super().program(argv)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.stdout.flush()
            os._exit(1)
        finally:
            sys.stdout.flush()
            os._exit(0)
