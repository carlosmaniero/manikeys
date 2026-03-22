import pyvista as pv
import pyfqmr
import numpy as np


def simplify(input_path: str, output_path: str, reduction: float = 0.5):
    mesh = pv.read(input_path)

    # In PyVista, faces is a flattened array: [3, v0, v1, v2, 3, v3, v4, v5, ...]
    faces = mesh.faces.reshape(-1, 4)[:, 1:4]
    num_faces = faces.shape[0]

    if num_faces < 100:
        if input_path != output_path:
            mesh.save(output_path)
        return

    mesh_simplifier = pyfqmr.Simplify()
    mesh_simplifier.setMesh(
        mesh.points.astype(np.float32), faces.astype(np.int32)
    )

    target_triangles = int(num_faces * (1 - reduction))

    mesh_simplifier.simplify_mesh(
        target_count=target_triangles,
        aggressiveness=7,
        preserve_border=True,
        verbose=False,
    )

    v_new, f_new, _ = mesh_simplifier.getMesh()

    # Rebuild PyVista mesh
    f_new_pv = np.column_stack((np.full(len(f_new), 3), f_new)).flatten()
    simplified_mesh = pv.PolyData(v_new, f_new_pv)
    simplified_mesh.save(output_path)
