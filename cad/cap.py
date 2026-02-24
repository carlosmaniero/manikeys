import openscad as osc
from models.projection import SphereProjection
from data.parameters import parameters
from data.layout import layout

fn = 20


def outer():
    obj = osc.cube(
        [
            parameters.caps.size + parameters.caps.border * 2,
            parameters.caps.size + parameters.caps.border * 2,
            parameters.caps.outer.thickness,
        ],
        center=True,
    )

    obj += [0, 0, parameters.caps.thickness]
    obj -= [0, 0, parameters.caps.outer.thickness]
    obj = osc.color(obj, "blue")
    obj = obj.fillet(parameters.caps.border / 4, fn=fn)

    return obj


def cap():
    body = outer()

    obj = osc.cube(
        [
            parameters.caps.size,
            parameters.caps.size,
            parameters.caps.thickness + parameters.globals.diff_offset,
        ],
        center=True,
    )
    obj += [0, 0, parameters.caps.thickness / 2]
    obj = osc.color(obj, "red")

    return body - obj


def assembly_grid(projection: SphereProjection):
    grid = []

    for column in layout.grid:
        for key in column:
            rotation = projection.project_rotation(key.position)

            grid.append(
                cap().rotate(rotation)
                + key.position
                + [0, 0, projection.radius]
            )

    return osc.union(*grid)
