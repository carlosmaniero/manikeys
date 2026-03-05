from context import injector
from cad.cap import CapCAD
from openscad_ext.slicer import slicer, Slice
import openscad as osc
import math

height = 180
depth = 100
radius = 300


def smooth_transition(f, h, t):
    t = max(0, min(1, t))
    v = t * t * (3 - 2 * t)

    def combined_func(x):
        return (1 - v) * f(x) + v * h(x)

    return combined_func


def smooth_transition_from_to(f, h, from_x, to_x):
    return lambda x: smooth_transition(f, h, (x - from_x) / (to_x - from_x))(x)


def get_sphere_lower_y(x, z):
    distance = math.sqrt(x**2 + z**2)

    if distance >= radius:
        return radius
    else:
        result = radius - math.sqrt(radius**2 - distance**2)
        if result > 33:
            return 33
        return result


def get_shape(x: float, z: float):
    transition_start = 65
    transition_end = 75
    start_fixed = get_sphere_lower_y(transition_start, -21)

    if x <= transition_start:
        return get_sphere_lower_y(x, z)
    return smooth_transition_from_to(
        lambda x: get_sphere_lower_y(x, z),
        lambda x: start_fixed + (x - transition_start) / 2,
        transition_start,
        transition_end,
    )(x)


def all_slices(z):
    r = 20
    x_delta = 0

    z_start = -20
    z_end = height + z_start
    dist_from_start = z - z_start
    dist_from_end = z_end - z
    relative_z = min(dist_from_start, dist_from_end)

    if relative_z < r:
        safe_rel_z = max(0.0, min(r, relative_z))
        x_delta = r - math.sqrt(r**2 - (r - safe_rel_z) ** 2)

    return Slice(
        upper=lambda x: get_shape(x, z),
        lower=lambda x: -15,
        x_range=(-40 + x_delta, depth - x_delta),
        slices=400,
    )


def main():
    return slicer(all_slices, z_range=(-20, height - 20), fn=400).rotate(
        [90, 0, 90]
    )


if __name__ == "__main__":
    cap_cad = injector.get(CapCAD)
    body = main()
    body = osc.color(body, "#333333")
    body |= cap_cad.assembly_grid()
    body = body.difference(cap_cad.cap_holes())
    body.show()
