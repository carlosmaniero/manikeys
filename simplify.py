import argparse
import meshlib.mrmeshpy as mrmeshpy
import os
import multiprocessing
import sys


def main():
    parser = argparse.ArgumentParser(description="Simplify mesh using meshlib")
    parser.add_argument("-i", "--input", required=True, help="Input mesh file")
    parser.add_argument(
        "-o", "--output", required=True, help="Output mesh file"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")

        parser.print_help()

        sys.exit(1)

    mesh = mrmeshpy.loadMesh(args.input)

    mesh.packOptimally()

    settings = mrmeshpy.DecimateSettings()

    settings.maxError = 0.05

    settings.subdivideParts = multiprocessing.cpu_count()

    mrmeshpy.decimateMesh(mesh, settings)

    mrmeshpy.saveMesh(mesh, args.output)


if __name__ == "__main__":
    main()
