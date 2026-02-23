from sphere_projection import SphereProjection
from collections import namedtuple
import openscad as osc

fn = 200

body_radius = osc.add_parameter("body_radius", 300)
body_diameter = body_radius * 2

keyboard_size = namedtuple("KEYBOARD_SIZE", ["width", "depth", "thickness"])(
    width=150, depth=130, thickness=5
)

projection = SphereProjection(body_radius)


def body_mask():
    center = [
        keyboard_size.width / 2,
        keyboard_size.depth / 2,
        keyboard_size.thickness / 2,
    ]

    [position, rotation] = projection.project_with_rotation(center)

    obj = osc.cube(
        [
            keyboard_size.width,
            keyboard_size.depth,
            body_radius,
        ],
        center=True,
    )

    obj += [0, 0, keyboard_size.thickness / 2]
    obj = osc.color(obj, "red")

    obj = obj.rotate(rotation)
    obj = obj.translate(position)

    return obj


def body():
    obj = osc.sphere(body_radius)
    obj += [0, 0, body_radius]

    internal_radius = body_radius - keyboard_size.thickness
    obj -= osc.sphere(internal_radius) + [0, 0, body_radius]

    return obj.intersection(body_mask())


def assembly():
    return body()
