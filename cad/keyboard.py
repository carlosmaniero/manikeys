from sphere_projection import SphereProjection
import openscad as osc
from data.parameters import parameters
from cad.cap import assembly_grid

projection = SphereProjection(parameters.body.radius)


center = [
    parameters.body.width / 2,
    parameters.body.depth / 2,
    parameters.body.thickness,
]


def body_mask():

    [position, rotation] = projection.project_with_rotation(center)

    obj = osc.cube(
        [
            parameters.body.width,
            parameters.body.depth,
            parameters.body.radius,
        ],
        center=True,
    )

    obj += [0, 0, parameters.body.thickness / 2]
    obj = osc.color(obj, "red")

    obj = obj.rotate(rotation)
    obj = obj.translate(position)

    return obj


def body():
    obj = osc.sphere(parameters.body.radius)
    obj += [0, 0, parameters.body.radius - parameters.body.thickness]

    internal_radius = parameters.body.radius
    obj -= osc.sphere(internal_radius) + [0, 0, parameters.body.radius]

    return obj.intersection(body_mask())


def assembly():
    return assembly_grid(projection)
