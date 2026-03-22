import meshlib.mrmeshpy as mrmeshpy
import multiprocessing


def simplify(input_path: str, output_path: str, max_error: float = 0.01):
    mesh = mrmeshpy.loadMesh(input_path)

    if mesh.topology.numValidFaces() < 100:
        if input_path != output_path:
            mrmeshpy.saveMesh(mesh, output_path)
        return

    mesh.packOptimally()

    settings = mrmeshpy.DecimateSettings()
    settings.maxError = max_error
    settings.subdivideParts = multiprocessing.cpu_count()

    mrmeshpy.decimateMesh(mesh, settings)
    mrmeshpy.saveMesh(mesh, output_path)
