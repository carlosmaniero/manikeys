import meshoptimizer as meshopt
import pyvista as pv
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

    points = mesh.points.astype(np.float32)
    indices = faces.astype(np.uint32).flatten()

    target_index_count = int(len(indices) * (1 - reduction))
    # Ensure it's a multiple of 3
    target_index_count = (target_index_count // 3) * 3

    destination = np.zeros(len(indices), dtype=np.uint32)

    # Use SIMPLIFY_LOCK_BORDER to preserve edges
    options = meshopt.SIMPLIFY_LOCK_BORDER

    count = meshopt.simplify(
        destination,
        indices,
        points,
        target_index_count=target_index_count,
        options=options,
    )

    new_indices = destination[:count]
    f_new = new_indices.reshape(-1, 3)

    # Rebuild PyVista mesh
    f_new_pv = np.column_stack((np.full(len(f_new), 3), f_new)).flatten()
    simplified_mesh = pv.PolyData(points, f_new_pv)

    # meshoptimizer doesn't remove unused vertices, so we should clean the mesh
    simplified_mesh = simplified_mesh.clean()

    simplified_mesh.save(output_path)
