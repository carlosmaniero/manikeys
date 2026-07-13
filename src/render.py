from __future__ import annotations
import sys
import numpy as np
import trimesh
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_3mf_to_trimesh
from structure.body.models import BodyModel
from core.trimesh_ext.object import TrimeshObject


@singleton
@inject
@dataclass
class RenderCAD(TrimeshObject):
    model: BodyModel

    def assemble(self) -> trimesh.Scene:
        left_scene = load_3mf_to_trimesh("build/main.3mf")

        # Define mirroring matrix across the X-axis
        mirror_matrix = np.eye(4)
        mirror_matrix[0, 0] = -1.0

        distance = self.model.end_x() + 200

        # Reconstruct left meshes and mirrored/translated right meshes
        scene = trimesh.Scene()

        # Handle geometries from left side
        for name, geom in left_scene.geometry.items():
            left_geom = geom.copy()
            left_geom.metadata["file_name"] = f"left_{name}"
            scene.add_geometry(left_geom, geom_name=f"left_{name}")

            # Create the mirrored right geometry
            right_geom = geom.copy()
            right_geom.apply_transform(mirror_matrix)
            # Invert faces to fix normal winding direction due to mirror
            right_geom.faces = np.fliplr(right_geom.faces)
            # Translate to the right side
            right_geom.apply_translation([distance, 0, 0])

            right_geom.metadata["file_name"] = f"right_{name}"
            scene.add_geometry(right_geom, geom_name=f"right_{name}")

        return scene


if __name__ == "__main__":
    render = injector.get(RenderCAD)
    render.program(sys.argv)
