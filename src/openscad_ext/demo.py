from .slicer import slicer, Slice
import math


def sphere_slices(z: float) -> Slice:
    radius = 25
    r_sq = radius**2 - (z - radius) ** 2
    r = math.sqrt(max(0.0, r_sq))

    r = max(r, 0.01)

    return Slice(
        upper=lambda x: math.sqrt(max(0.0, r**2 - x**2)),
        lower=lambda x: -math.sqrt(max(0.0, r**2 - x**2)),
        x_range=(-r, r),
        slices=100,
    )


def show_sphere():
    slicer(sphere_slices, z_range=(0, 50), fn=100).show()
