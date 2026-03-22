import argparse
import os
import sys

from simplifiers import pyfqmr, meshlib, meshoptimizer


def main():
    parser = argparse.ArgumentParser(description="Simplify mesh using meshlib")
    parser.add_argument("-i", "--input", required=True, help="Input mesh file")
    parser.add_argument(
        "-o", "--output", required=True, help="Output mesh file"
    )
    parser.add_argument(
        "-s",
        "--simplifier",
        choices=["pyfqmr", "meshlib", "meshoptimizer"],
        default="meshlib",
        help="Simplifier to use (default: meshlib)",
    )

    parser.add_argument(
        "-r",
        "--reduction",
        type=float,
        default=0.5,
        help="Reduction ratio (0.0 to 1.0) for pyfqmr and meshoptimizer (default: 0.5)",
    )
    parser.add_argument(
        "-e",
        "--max-error",
        type=float,
        default=0.01,
        help="Max error for meshlib (default: 0.01)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        parser.print_help()
        sys.exit(1)

    if args.simplifier == "pyfqmr":
        pyfqmr.simplify(args.input, args.output, reduction=args.reduction)
    elif args.simplifier == "meshlib":
        meshlib.simplify(args.input, args.output, max_error=args.max_error)
    elif args.simplifier == "meshoptimizer":
        meshoptimizer.simplify(
            args.input, args.output, reduction=args.reduction
        )


if __name__ == "__main__":
    main()
