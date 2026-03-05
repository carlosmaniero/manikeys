from openscad_ext.loft import loft, Profile
import math


def sphere_sections(z: float) -> Profile:
    radius = 25
    r_sq = radius**2 - (z - radius) ** 2
    r = math.sqrt(max(0.0, r_sq))

    r = max(r, 0.01)

    return Profile(
        upper=lambda x: math.sqrt(max(0.0, r**2 - x**2)),
        lower=lambda x: -math.sqrt(max(0.0, r**2 - x**2)),
        span=(-r, r),
        segments=100,
    )


def show_sphere():
    loft(sphere_sections, span=(0, 50), fn=100).show()


if __name__ == "__main__":
    show_sphere()
