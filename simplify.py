import argparse
import meshlib.mrmeshpy as mrmesh
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Simplify mesh using meshlib")
    parser.add_argument("-i", "--input", required=True, help="Input mesh file")
    parser.add_argument(
        "-o", "--output", required=True, help="Output mesh file"
    )
    parser.add_argument(
        "-p",
        "--percentage",
        type=float,
        default=0.5,
        help="Target percentage of faces (0.0 to 1.0)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        sys.exit(1)

    # Load mesh
    print(f"Loading {args.input}")
    try:
        mesh = mrmesh.loadMesh(args.input)
    except Exception as e:
        print(f"Failed to load mesh with generic loadMesh: {e}")
        try:
            print("Trying loadASCIIStl...")
            mesh = mrmesh.loadASCIIStl(args.input)
        except Exception as e2:
            print(f"Failed to load mesh with loadASCIIStl: {e2}")
            sys.exit(1)

    # Get current face count
    face_count = mesh.topology.numValidFaces()
    if face_count == 0:
        print("Mesh has no faces, skipping simplification.")
        mrmesh.saveMesh(mesh, args.output)
        return

    target_count = int(face_count * args.percentage)
    max_deleted = face_count - target_count

    print(
        f"Simplifying: {face_count} -> {target_count} faces (deleting up to {max_deleted})"
    )

    # Decimation settings
    settings = mrmesh.DecimateSettings()
    settings.maxDeletedFaces = max_deleted
    settings.strategy = mrmesh.DecimateStrategy.ShortestEdgeFirst
    settings.packMesh = True  # Try to keep it clean

    # Perform decimation
    try:
        mrmesh.decimateMesh(mesh, settings)
    except Exception as e:
        print(f"Decimation failed: {e}")
        sys.exit(1)

    # Save output
    print(f"Saving to {args.output}")
    try:
        mrmesh.saveMesh(mesh, args.output)
    except Exception as e:
        print(f"Failed to save mesh: {e}")
        sys.exit(1)
    print("Done")


if __name__ == "__main__":
    main()
